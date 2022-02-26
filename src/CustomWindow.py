from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QListWidgetItem, QMessageBox, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QEnterEvent
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

        # about drag window
        self.isDraging = False

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
        if self.isMaximized() == True:
            # normalize
            self.showNormal()
            self.outermost_layout.setContentsMargins(5, 5, 5, 5)
        else:
            # maximize
            self.restoreSize = self.size()
            self.restorePos = self.pos()
            self.setCursor(Qt.ArrowCursor)
            self.outermost_layout.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()

    def mousePressEvent(self, QMouseEvent):
        """
        Only can be drag when using left button and click the title bar
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.title_bar_height:
            self.isDraging = True
            self.startMovePosition = QMouseEvent.globalPos()
            self.startMousePosition = QMouseEvent.pos()

        if self.edge_scaling and QMouseEvent.button() == Qt.MouseButton.LeftButton and (QMouseEvent.x() <= self.dragPadding or
                                                                                        QMouseEvent.y() <= self.dragPadding or
                                                                                        self.size().width() - QMouseEvent.x() <= self.dragPadding or
                                                                                        self.size().height() - QMouseEvent.y() <= self.dragPadding):
            self.isScaling = True
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
        self.isDraging = False
        if self.edge_scaling:
            self.isScaling = False

    def mouseMoveEvent(self, QMouseEvent):
        """
        Drag and scaling custom window
        """
        if self.isMaximized() == False and self.edge_scaling:
            # when not maximize
            # if not scaling then judging where mouse is
            # or scaling then scaling the window
            if not self.isScaling:
                if QMouseEvent.x() <= self.dragPadding and QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeFDiagCursor)
                    self.scalingDirection = ScalingDirection.left_top
                elif QMouseEvent.x() <= self.dragPadding and self.size().height() - QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeBDiagCursor)
                    self.scalingDirection = ScalingDirection.left_bottom
                elif self.size().width() - QMouseEvent.x() <= self.dragPadding and QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeBDiagCursor)
                    self.scalingDirection = ScalingDirection.right_top
                elif self.size().width() - QMouseEvent.x() <= self.dragPadding and self.size().height() - QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeFDiagCursor)
                    self.scalingDirection = ScalingDirection.right_bottom
                elif QMouseEvent.x() <= self.dragPadding:
                    self.setCursor(Qt.SizeHorCursor)
                    self.scalingDirection = ScalingDirection.left
                elif self.size().width() - QMouseEvent.x() <= self.dragPadding:
                    self.setCursor(Qt.SizeHorCursor)
                    self.scalingDirection = ScalingDirection.right
                elif QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeVerCursor)
                    self.scalingDirection = ScalingDirection.top
                elif self.size().height() - QMouseEvent.y() <= self.dragPadding:
                    self.setCursor(Qt.SizeVerCursor)
                    self.scalingDirection = ScalingDirection.bottom
                else:
                    self.scalingDirection = ScalingDirection.center
                    self.setCursor(Qt.ArrowCursor)
            else:
                curr_size = self.size()
                curr_pos = self.pos()
                if self.scalingDirection == ScalingDirection.left:
                    curr_size.setWidth(
                        max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                    curr_pos.setX(min(curr_pos.x() + QMouseEvent.x(),
                                      self.rightX))
                    self.resize(curr_size)
                    self.move(curr_pos)
                elif self.scalingDirection == ScalingDirection.right:
                    curr_size.setWidth(
                        max(QMouseEvent.x(), self.minimumWidth()))
                    self.resize(curr_size)
                elif self.scalingDirection == ScalingDirection.top:
                    curr_size.setHeight(
                        max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                    curr_pos.setY(
                        min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                    self.resize(curr_size)
                    self.move(curr_pos)
                elif self.scalingDirection == ScalingDirection.bottom:
                    curr_size.setHeight(
                        max(QMouseEvent.y(), self.minimumHeight()))
                    self.resize(curr_size)
                elif self.scalingDirection == ScalingDirection.left_top:
                    curr_size.setWidth(
                        max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                    curr_size.setHeight(
                        max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                    curr_pos.setX(
                        min(curr_pos.x() + QMouseEvent.x(), self.rightX))
                    curr_pos.setY(
                        min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                    self.resize(curr_size)
                    self.move(curr_pos)
                elif self.scalingDirection == ScalingDirection.left_bottom:
                    curr_size.setWidth(
                        max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                    curr_size.setHeight(
                        max(QMouseEvent.y(), self.minimumHeight()))
                    curr_pos.setX(min(curr_pos.x() + QMouseEvent.x(),
                                      self.rightX))
                    self.resize(curr_size)
                    self.move(curr_pos)
                elif self.scalingDirection == ScalingDirection.right_top:
                    curr_size.setHeight(
                        max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                    curr_size.setWidth(
                        max(QMouseEvent.x(), self.minimumWidth()))
                    curr_pos.setY(
                        min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                    self.resize(curr_size)
                    self.move(curr_pos)
                elif self.scalingDirection == ScalingDirection.right_bottom:
                    curr_size.setWidth(
                        max(QMouseEvent.x(), self.minimumWidth()))
                    curr_size.setHeight(
                        max(QMouseEvent.y(), self.minimumHeight()))
                    self.resize(curr_size)
                else:
                    self.setCursor(Qt.ArrowCursor)
                return

        if self.isDraging:
            if self.isMaximized() == True:
                """
                when window is maximum
                restore the window size and maintain the mouse relative position
                """
                # calculate mouse position rate
                pos_rate = QMouseEvent.x() / self.size().width()
                # calculate the distance from left to mouse
                normal_pos = self.restoreSize.width() * pos_rate
                # set the mouse position
                mouse_pos = QMouseEvent.pos()
                mouse_pos.setX(normal_pos)
                self.showMaximizeOrNormalize()
                # calculate the window global position
                final_pos = QMouseEvent.globalPos()
                final_pos.setX(final_pos.x() - normal_pos)
                self.move(final_pos)
                self.startMovePosition = QMouseEvent.globalPos()
                self.startMousePosition = mouse_pos
                self.isScaling = False
            self.setCursor(Qt.ArrowCursor)
            MovePos = QMouseEvent.globalPos()
            self.move(MovePos - self.startMousePosition)
            self.startMovePosition = MovePos

    def eventFilter(self, watched, event) -> bool:
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
