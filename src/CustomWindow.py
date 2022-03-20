from ctypes.wintypes import MSG
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from win32api import *
from win32gui import *
from win32con import *


class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # set these parameters first
        self.maximize = True
        self.edge_scaling = False
        self.title_bar_height = None
        self.outermost_layout = None
        self.main_widget = None
        self.toggle_pressed = False
        self.prePos = None

        # set window flags
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint |
                            Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # set effect shadow
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(10)
        self.effect_shadow.setColor(Qt.black)

        if self.edge_scaling:
            # set edge scaling parameters
            self.dragPadding = 5

    def drawShadow(self):
        """
        Draw window shadow
        """
        self.outermost_layout.setContentsMargins(5, 5, 5, 5)
        self.main_widget.setGraphicsEffect(self.effect_shadow)

    def showMaximizeOrNormalize(self):
        """
        Maximize or normalize the winodw
        """
        if self.window().isMaximized():
            # normalize
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, QMouseEvent):
        """
        Only can be drag when using left button and click the title bar
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.title_bar_height:
            ReleaseCapture()
            SendMessage(self.window().winId(), WM_SYSCOMMAND,
                        SC_MOVE + HTCAPTION, 0)
            QMouseEvent.ignore()

    def mouseDoubleClickEvent(self, QMouseEvent):
        """
        Double click to maximum and minimum the window
        """
        # only activate when set flag to True
        if self.maximize and QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.title_bar_height:
            self.showMaximizeOrNormalize()

    def togglePressedEvent(self):
        if not self.window().isMaximized():
            self.toggle_pressed = True

    def toggleReleasedEvent(self):
        self.toggle_pressed = False

    def nativeEvent(self, eventType, message):
        msg = MSG.from_address(message.__int__())

        if self.maximize:
            if self.window().isMaximized():
                maximize_icon = QIcon()
                maximize_icon.addFile(
                    u":/imgs/imgs/windowed.png", QSize(), QIcon.Normal, QIcon.Off)
                self.ui.btn_max.setIcon(maximize_icon)
                self.outermost_layout.setContentsMargins(0, 0, 0, 0)
            else:
                windowed_icon = QIcon()
                windowed_icon.addFile(
                    u":/imgs/imgs/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
                self.ui.btn_max.setIcon(windowed_icon)
                self.outermost_layout.setContentsMargins(5, 5, 5, 5)

        if self.edge_scaling and not self.window().isMaximized() and msg.message == WM_NCHITTEST:
            r = self.devicePixelRatioF()
            xPos = (LOWORD(msg.lParam) - self.frameGeometry().x()*r) % 65536
            yPos = HIWORD(msg.lParam) - self.frameGeometry().y()*r
            w, h = self.width()*r, self.height()*r
            lx = xPos < self.dragPadding
            rx = xPos > w - self.dragPadding
            ty = yPos < self.dragPadding
            by = yPos > h - self.dragPadding

            if (lx and ty):
                return True, HTTOPLEFT
            elif (rx and by):
                return True, HTBOTTOMRIGHT
            elif (rx and ty):
                return True, HTTOPRIGHT
            elif (lx and by):
                return True, HTBOTTOMLEFT
            elif ty:
                return True, HTTOP
            elif by:
                return True, HTBOTTOM
            elif lx:
                return True, HTLEFT
            elif rx:
                return True, HTRIGHT
