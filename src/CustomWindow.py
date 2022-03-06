from ctypes.wintypes import MSG
from pickle import TRUE
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QEnterEvent, QIcon
from win32api import *
from win32gui import *
import win32con
from enum import Enum


class ScalingDirection(Enum):
    # Directions:
    # 1   2   3
    # 4   5   6
    # 7   8   9
    left_top = 1
    top = 2
    right_top = 3
    left = 4
    center = 5
    right = 6
    left_bottom = 7
    bottom = 8
    right_bottom = 9


class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # set these parameters first
        self.maximize = True
        self.edge_scaling = True
        self.title_bar_height = None
        self.outermost_layout = None
        self.main_widget = None

        # set window flags
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # set effect shadow
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(10)
        self.effect_shadow.setColor(Qt.black)

        if self.edge_scaling:
            # set edge scaling parameters
            self.setMouseTracking(True)
            self.dragPadding = 5
            self.isScaling = False
            self.scalingDirection = ScalingDirection.center

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
            self.outermost_layout.setContentsMargins(5, 5, 5, 5)
            windowed_icon = QIcon()
            windowed_icon.addFile(
                u":/imgs/imgs/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
            self.ui.btn_max.setIcon(windowed_icon)
        else:
            # maximize
            self.restoreSize = self.size()
            self.restorePos = self.pos()
            self.setCursor(Qt.ArrowCursor)
            self.outermost_layout.setContentsMargins(0, 0, 0, 0)
            maximize_icon = QIcon()
            maximize_icon.addFile(
                u":/imgs/imgs/windowed.png", QSize(), QIcon.Normal, QIcon.Off)
            self.ui.btn_max.setIcon(maximize_icon)
            self.window().showMaximized()

    def mousePressEvent(self, QMouseEvent):
        """
        Only can be drag when using left button and click the title bar
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.title_bar_height:
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            QMouseEvent.ignore()

        if self.edge_scaling and QMouseEvent.button() == Qt.MouseButton.LeftButton and (QMouseEvent.x() <= self.dragPadding or
                                                                                        QMouseEvent.y() <= self.dragPadding or
                                                                                        self.size().width() - QMouseEvent.x() <= self.dragPadding or
                                                                                        self.size().height() - QMouseEvent.y() <= self.dragPadding):
            # self.isScaling = True
            self.btnY = self.pos().y() + self.size().height() - self.minimumHeight()
            self.rightX = self.pos().x() + self.size().width() - self.minimumWidth()

    def mouseDoubleClickEvent(self, QMouseEvent):
        """
        Double click to maximum and minimum the window
        """
        # only activate when set flag to True
        if self.maximize and QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.title_bar_height:
            self.showMaximizeOrNormalize()

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Release the button
        """
        if self.edge_scaling:
            self.isScaling = False

    def nativeEvent(self, eventType, message):
        msg = MSG.from_address(message.__int__())

        if msg.message == win32con.WM_NCHITTEST:
            xPos = (LOWORD(msg.lParam) - self.frameGeometry().x()) % 65536
            yPos = HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()
            lx = xPos < self.dragPadding
            rx = xPos > w - self.dragPadding
            ty = yPos < self.dragPadding
            by = yPos > h - self.dragPadding

            if (lx and ty):
                return True, win32con.HTTOPLEFT
            elif (rx and by):
                return True, win32con.HTBOTTOMRIGHT
            elif (rx and ty):
                return True, win32con.HTTOPRIGHT
            elif (lx and by):
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT

    def eventFilter(self, watched, event) -> bool:
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
