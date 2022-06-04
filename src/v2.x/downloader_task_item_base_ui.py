# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downloadTaskItem.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QProgressBar, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(432, 136)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.FItem = QFrame(Form)
        self.FItem.setObjectName(u"FItem")
        self.FItem.setFrameShape(QFrame.StyledPanel)
        self.FItem.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.FItem)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.FItemCover = QFrame(self.FItem)
        self.FItemCover.setObjectName(u"FItemCover")
        self.FItemCover.setMinimumSize(QSize(180, 100))
        self.FItemCover.setMaximumSize(QSize(180, 100))
        self.FItemCover.setFrameShape(QFrame.StyledPanel)
        self.FItemCover.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.FItemCover)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 5, 5, 5)
        self.LItemCover = QLabel(self.FItemCover)
        self.LItemCover.setObjectName(u"LItemCover")
        self.LItemCover.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.LItemCover)


        self.horizontalLayout_2.addWidget(self.FItemCover)

        self.FItemInfo = QFrame(self.FItem)
        self.FItemInfo.setObjectName(u"FItemInfo")
        self.FItemInfo.setFrameShape(QFrame.StyledPanel)
        self.FItemInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.FItemInfo)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 5, -1, 5)
        self.FItemTitle = QFrame(self.FItemInfo)
        self.FItemTitle.setObjectName(u"FItemTitle")
        self.FItemTitle.setFrameShape(QFrame.StyledPanel)
        self.FItemTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.FItemTitle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.LItemTitle = QLabel(self.FItemTitle)
        self.LItemTitle.setObjectName(u"LItemTitle")
        self.LItemTitle.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.LItemTitle)


        self.verticalLayout.addWidget(self.FItemTitle)

        self.FItemStatus = QFrame(self.FItemInfo)
        self.FItemStatus.setObjectName(u"FItemStatus")
        self.FItemStatus.setFrameShape(QFrame.StyledPanel)
        self.FItemStatus.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.FItemStatus)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.LItemStatus = QLabel(self.FItemStatus)
        self.LItemStatus.setObjectName(u"LItemStatus")
        self.LItemStatus.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.LItemStatus)

        self.LItemCount = QLabel(self.FItemStatus)
        self.LItemCount.setObjectName(u"LItemCount")
        self.LItemCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.LItemCount)


        self.verticalLayout.addWidget(self.FItemStatus)

        self.FItemProcess = QFrame(self.FItemInfo)
        self.FItemProcess.setObjectName(u"FItemProcess")
        self.FItemProcess.setFrameShape(QFrame.StyledPanel)
        self.FItemProcess.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.FItemProcess)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, -1, 0, 0)
        self.PbProgress = QProgressBar(self.FItemProcess)
        self.PbProgress.setObjectName(u"PbProgress")
        self.PbProgress.setMaximumSize(QSize(16777215, 5))
        self.PbProgress.setValue(24)
        self.PbProgress.setTextVisible(False)

        self.horizontalLayout_5.addWidget(self.PbProgress)


        self.verticalLayout.addWidget(self.FItemProcess)


        self.horizontalLayout_2.addWidget(self.FItemInfo)


        self.horizontalLayout.addWidget(self.FItem)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.FItem.setProperty("status", "")
        self.LItemCover.setText("")
        self.LItemTitle.setText("")
        self.LItemStatus.setText("")
        self.LItemCount.setText("")
    # retranslateUi

