import sys
from PySide6.QtCore import Qt
from settings_base_ui import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget
from terminal_downloader import *


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_min.clicked.connect(self.showMinimized)
        self.setMouseTracking(True)
        self.isPressed = False
        self.padding = 3

    def mousePressEvent(self, QMouseEvent):
        """
        only can be drag when using left button and click the bar
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.ui.title_bar.height():
            self.isPressed = True
            self.startMovePosition = QMouseEvent.globalPos()
            self.startMousePosition = QMouseEvent.pos()

    def mouseReleaseEvent(self, QMouseEvent):
        """
        release the button
        """
        self.isPressed = False

    def mouseMoveEvent(self, QMouseEvent):
        """
        drag custom title bar
        """
        if self.isPressed:
            if self.isMaximized() == True:
                """
                when window is maximum
                restore the window size and maintain the mouse relative position
                """
                self.showNormal()
                # calculate mouse position rate
                pos_rate = QMouseEvent.x() / self.size().width()
                # calculate the distance from left to mouse
                normal_pos = self.restoreSize.width() * pos_rate
                # set the mouse position
                mouse_pos = QMouseEvent.pos()
                mouse_pos.setX(normal_pos)
                # resize the window
                self.resize(self.restoreSize)
                # calculate the window global position
                final_pos = QMouseEvent.globalPos()
                final_pos.setX(final_pos.x() - normal_pos)
                self.move(final_pos)
                self.startMovePosition = QMouseEvent.globalPos()
                self.startMousePosition = mouse_pos
            MovePos = QMouseEvent.globalPos()
            self.move(MovePos - self.startMousePosition)
            self.startMovePosition = MovePos


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = SettingWindow()
    widget.show()

    sys.exit(app.exec())
