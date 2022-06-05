# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'taskDetailWindow.ui'
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
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(562, 763)
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
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.FEpisodeList = QFrame(self.FContentBar)
        self.FEpisodeList.setObjectName(u"FEpisodeList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.FEpisodeList.sizePolicy().hasHeightForWidth())
        self.FEpisodeList.setSizePolicy(sizePolicy1)
        self.FEpisodeList.setMinimumSize(QSize(550, 0))
        self.FEpisodeList.setMaximumSize(QSize(1000, 16777215))
        self.FEpisodeList.setFrameShape(QFrame.StyledPanel)
        self.FEpisodeList.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.FEpisodeList)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.FChapterTitle = QFrame(self.FEpisodeList)
        self.FChapterTitle.setObjectName(u"FChapterTitle")
        self.FChapterTitle.setFrameShape(QFrame.StyledPanel)
        self.FChapterTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.FChapterTitle)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.LChapterTitle = QLabel(self.FChapterTitle)
        self.LChapterTitle.setObjectName(u"LChapterTitle")

        self.horizontalLayout_9.addWidget(self.LChapterTitle)

        self.FChapterBtns = QFrame(self.FChapterTitle)
        self.FChapterBtns.setObjectName(u"FChapterBtns")
        self.FChapterBtns.setMaximumSize(QSize(150, 16777215))
        self.FChapterBtns.setFrameShape(QFrame.StyledPanel)
        self.FChapterBtns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.FChapterBtns)
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.PbStartResumeAll = QPushButton(self.FChapterBtns)
        self.PbStartResumeAll.setObjectName(u"PbStartResumeAll")
        sizePolicy.setHeightForWidth(self.PbStartResumeAll.sizePolicy().hasHeightForWidth())
        self.PbStartResumeAll.setSizePolicy(sizePolicy)
        self.PbStartResumeAll.setMinimumSize(QSize(0, 30))
        self.PbStartResumeAll.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_8.addWidget(self.PbStartResumeAll)

        self.PbParsePage = QPushButton(self.FChapterBtns)
        self.PbParsePage.setObjectName(u"PbParsePage")
        sizePolicy.setHeightForWidth(self.PbParsePage.sizePolicy().hasHeightForWidth())
        self.PbParsePage.setSizePolicy(sizePolicy)
        self.PbParsePage.setMinimumSize(QSize(0, 30))
        self.PbParsePage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_8.addWidget(self.PbParsePage)


        self.horizontalLayout_9.addWidget(self.FChapterBtns)


        self.verticalLayout_6.addWidget(self.FChapterTitle)

        self.FChapterList = QFrame(self.FEpisodeList)
        self.FChapterList.setObjectName(u"FChapterList")
        self.FChapterList.setFrameShape(QFrame.StyledPanel)
        self.FChapterList.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.FChapterList)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.LwChapterList = QListWidget(self.FChapterList)
        self.LwChapterList.setObjectName(u"LwChapterList")

        self.verticalLayout_7.addWidget(self.LwChapterList)


        self.verticalLayout_6.addWidget(self.FChapterList)


        self.verticalLayout_2.addWidget(self.FEpisodeList, 0, Qt.AlignHCenter)


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
        self.LChapterTitle.setText("")
        self.PbStartResumeAll.setText("")
        self.PbParsePage.setText("")
        self.LStatus.setText("")
    # retranslateUi

