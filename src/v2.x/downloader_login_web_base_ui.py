# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginWebWindow.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 550)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.FTitleBar = QFrame(self.centralwidget)
        self.FTitleBar.setObjectName(u"FTitleBar")
        self.FTitleBar.setMaximumSize(QSize(16777215, 35))
        self.FTitleBar.setFrameShape(QFrame.StyledPanel)
        self.FTitleBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.FTitleBar)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.FIcon = QFrame(self.FTitleBar)
        self.FIcon.setObjectName(u"FIcon")
        self.FIcon.setMaximumSize(QSize(32, 35))
        self.FIcon.setFrameShape(QFrame.StyledPanel)
        self.FIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.FIcon)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.LIcon = QLabel(self.FIcon)
        self.LIcon.setObjectName(u"LIcon")
        self.LIcon.setMaximumSize(QSize(32, 32))
        self.LIcon.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.LIcon)


        self.horizontalLayout_4.addWidget(self.FIcon)

        self.FTitle = QFrame(self.FTitleBar)
        self.FTitle.setObjectName(u"FTitle")
        self.FTitle.setFrameShape(QFrame.StyledPanel)
        self.FTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.FTitle)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.LTitle = QLabel(self.FTitle)
        self.LTitle.setObjectName(u"LTitle")

        self.horizontalLayout_2.addWidget(self.LTitle)


        self.horizontalLayout_4.addWidget(self.FTitle)

        self.FBtns = QFrame(self.FTitleBar)
        self.FBtns.setObjectName(u"FBtns")
        self.FBtns.setMaximumSize(QSize(180, 16777215))
        self.FBtns.setFrameShape(QFrame.StyledPanel)
        self.FBtns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.FBtns)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.PbMinimize = QPushButton(self.FBtns)
        self.PbMinimize.setObjectName(u"PbMinimize")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PbMinimize.sizePolicy().hasHeightForWidth())
        self.PbMinimize.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.PbMinimize)

        self.PbMaximizeRestore = QPushButton(self.FBtns)
        self.PbMaximizeRestore.setObjectName(u"PbMaximizeRestore")
        sizePolicy.setHeightForWidth(self.PbMaximizeRestore.sizePolicy().hasHeightForWidth())
        self.PbMaximizeRestore.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.PbMaximizeRestore)

        self.PbClose = QPushButton(self.FBtns)
        self.PbClose.setObjectName(u"PbClose")
        sizePolicy.setHeightForWidth(self.PbClose.sizePolicy().hasHeightForWidth())
        self.PbClose.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.PbClose)


        self.horizontalLayout_4.addWidget(self.FBtns)


        self.verticalLayout.addWidget(self.FTitleBar)

        self.FContentBar = QFrame(self.centralwidget)
        self.FContentBar.setObjectName(u"FContentBar")
        self.FContentBar.setFrameShape(QFrame.StyledPanel)
        self.FContentBar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.FContentBar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.FInstructions = QFrame(self.FContentBar)
        self.FInstructions.setObjectName(u"FInstructions")
        self.FInstructions.setMaximumSize(QSize(16777215, 40))
        self.FInstructions.setFrameShape(QFrame.StyledPanel)
        self.FInstructions.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.FInstructions)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.LInstructions = QLabel(self.FInstructions)
        self.LInstructions.setObjectName(u"LInstructions")

        self.horizontalLayout_6.addWidget(self.LInstructions)


        self.verticalLayout_2.addWidget(self.FInstructions)

        self.FWebPage = QFrame(self.FContentBar)
        self.FWebPage.setObjectName(u"FWebPage")
        self.FWebPage.setFrameShape(QFrame.StyledPanel)
        self.FWebPage.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.FWebPage)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout_2.addWidget(self.FWebPage)


        self.verticalLayout.addWidget(self.FContentBar)

        self.FStatusBar = QFrame(self.centralwidget)
        self.FStatusBar.setObjectName(u"FStatusBar")
        self.FStatusBar.setMaximumSize(QSize(16777215, 25))
        self.FStatusBar.setFrameShape(QFrame.StyledPanel)
        self.FStatusBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.FStatusBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.LStatus = QLabel(self.FStatusBar)
        self.LStatus.setObjectName(u"LStatus")

        self.horizontalLayout_5.addWidget(self.LStatus)


        self.verticalLayout.addWidget(self.FStatusBar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LIcon.setText("")
        self.LTitle.setText("")
        self.PbMinimize.setText("")
        self.PbMaximizeRestore.setText("")
        self.PbClose.setText("")
        self.LInstructions.setText("")
        self.LStatus.setText("")
    # retranslateUi

