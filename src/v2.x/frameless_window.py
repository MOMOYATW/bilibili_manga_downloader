import os
from ctypes import POINTER, cast


from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QMainWindow

# only for windows
from ctypes.wintypes import MSG
from win32 import win32api, win32gui
from win32.lib import win32con

# import windoweffect
from window_effect import WindowEffect
from c_structures import MINMAXINFO, NCCALCSIZE_PARAMS

# import for title bar
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture


class FramelessWindowBase(QMainWindow):
    """
    Frameless Window
    """

    BORDER_WIDTH = 5
    TITLEBAR_HEIGHT = 35

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def resizeEvent(self, event) -> None:
        return super().resizeEvent(event)

    def _isWindowMaximized(self, hWnd):
        return self.isMaximized()

    # title bar
    def mouseDoubleClickEvent(self, event) -> None:
        """
        Toggles the maximization state of th window
        """
        if event.button() != Qt.LeftButton:
            return

        if not self._isTitlebarRegion(event.pos()):
            return

        self.toggleMaxState()

    def toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
            # change the icon of maxBtn
            self.changeIconMaximized()
        else:
            self.window().showMaximized()
            self.changeIconNormalized()

    def mousePressEvent(self, event) -> None:
        """ Move the window """
        if not self._isTitlebarRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE + win32con.HTCAPTION, 0)
        event.ignore()

    def _isTitlebarRegion(self, pos):
        """
        Check if mouse is in the title bar
        """
        return 0 < pos.y() < self.TITLEBAR_HEIGHT

    def changeIconMaximized(self):
        pass

    def changeIconNormalized(self):
        pass


class WindowsFramelessWindow(FramelessWindowBase):
    """
    Frameless Window for Windows System
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.__monitorInfo = None
        self.windowEffect = WindowEffect()

        # remove window border
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.addShadowEffect(self.winId())

        self.windowHandle().screenChanged.connect(self.__onScreenChanged)

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if self._isWindowMaximized(msg.hWnd):
                self.__monitorNCCALCSIZE(msg)
            return True, 0
        elif msg.message == win32con.WM_GETMINMAXINFO:
            if self._isWindowMaximized(msg.hWnd):
                window_rect = win32gui.GetWindowRect(msg.hWnd)
                if not window_rect:
                    return False, 0

                # get the monitor handle
                monitor = win32api.MonitorFromRect(window_rect)
                if not monitor:
                    return False, 0

                # get the monitor info
                __monitorInfo = win32api.GetMonitorInfo(monitor)
                monitor_rect = __monitorInfo['Monitor']
                work_area = __monitorInfo['Work']

                # convert lParam to MINMAXINFO pointer
                info = cast(msg.lParam, POINTER(MINMAXINFO)).contents

                # adjust the size of window
                info.ptMaxSize.x = work_area[2] - work_area[0]
                info.ptMaxSize.y = work_area[3] - work_area[1]
                info.ptMaxTrackSize.x = info.ptMaxSize.x
                info.ptMaxTrackSize.y = info.ptMaxSize.y

                # modify the upper left coordinate
                info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                return True, 1

        return QWidget.nativeEvent(self, eventType, message)

    def _isWindowMaximized(self, hWnd) -> bool:
        # GetWindowPlacement() returns the display state of the window and the restored,
        # maximized and minimized window position. The return value is tuple
        windowPlacement = win32gui.GetWindowPlacement(hWnd)
        if not windowPlacement:
            return False

        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def __monitorNCCALCSIZE(self, msg):
        """ Adjust the size of window """
        monitor = win32api.MonitorFromWindow(msg.hWnd)

        # If the display information is not saved, return directly
        if monitor is None and not self.__monitorInfo:
            return
        elif monitor is not None:
            self.__monitorInfo = win32api.GetMonitorInfo(monitor)

        # adjust the size of window
        params = cast(msg.lParam, POINTER(NCCALCSIZE_PARAMS)).contents
        params.rgrc[0].left = self.__monitorInfo['Work'][0]
        params.rgrc[0].top = self.__monitorInfo['Work'][1]
        params.rgrc[0].right = self.__monitorInfo['Work'][2]
        params.rgrc[0].bottom = self.__monitorInfo['Work'][3]

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
