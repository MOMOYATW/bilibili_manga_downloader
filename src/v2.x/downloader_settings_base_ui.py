# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 350)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(500, 350))
        MainWindow.setMaximumSize(QSize(500, 350))
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
        self.FBtns.setMaximumSize(QSize(120, 16777215))
        self.FBtns.setFrameShape(QFrame.StyledPanel)
        self.FBtns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.FBtns)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.PbMinimize = QPushButton(self.FBtns)
        self.PbMinimize.setObjectName(u"PbMinimize")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PbMinimize.sizePolicy().hasHeightForWidth())
        self.PbMinimize.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.PbMinimize)

        self.PbClose = QPushButton(self.FBtns)
        self.PbClose.setObjectName(u"PbClose")
        sizePolicy1.setHeightForWidth(self.PbClose.sizePolicy().hasHeightForWidth())
        self.PbClose.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.PbClose)


        self.horizontalLayout_4.addWidget(self.FBtns)


        self.verticalLayout.addWidget(self.FTitleBar)

        self.FContentBar = QFrame(self.centralwidget)
        self.FContentBar.setObjectName(u"FContentBar")
        self.FContentBar.setMinimumSize(QSize(500, 0))
        self.FContentBar.setFrameShape(QFrame.StyledPanel)
        self.FContentBar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.FContentBar)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.FTabMenu = QFrame(self.FContentBar)
        self.FTabMenu.setObjectName(u"FTabMenu")
        self.FTabMenu.setFrameShape(QFrame.StyledPanel)
        self.FTabMenu.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.FTabMenu)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.FMenuBar = QFrame(self.FTabMenu)
        self.FMenuBar.setObjectName(u"FMenuBar")
        self.FMenuBar.setFrameShape(QFrame.StyledPanel)
        self.FMenuBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.FMenuBar)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.FMenuBtns = QFrame(self.FMenuBar)
        self.FMenuBtns.setObjectName(u"FMenuBtns")
        self.FMenuBtns.setFrameShape(QFrame.StyledPanel)
        self.FMenuBtns.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.FMenuBtns)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.PbDownloadPage = QPushButton(self.FMenuBtns)
        self.PbDownloadPage.setObjectName(u"PbDownloadPage")
        self.PbDownloadPage.setMinimumSize(QSize(80, 40))

        self.verticalLayout_5.addWidget(self.PbDownloadPage)

        self.PbSpiderPage = QPushButton(self.FMenuBtns)
        self.PbSpiderPage.setObjectName(u"PbSpiderPage")
        self.PbSpiderPage.setMinimumSize(QSize(80, 40))

        self.verticalLayout_5.addWidget(self.PbSpiderPage)

        self.PbGeneralPage = QPushButton(self.FMenuBtns)
        self.PbGeneralPage.setObjectName(u"PbGeneralPage")
        self.PbGeneralPage.setMinimumSize(QSize(80, 40))

        self.verticalLayout_5.addWidget(self.PbGeneralPage)

        self.PbAboutPage = QPushButton(self.FMenuBtns)
        self.PbAboutPage.setObjectName(u"PbAboutPage")
        self.PbAboutPage.setMinimumSize(QSize(80, 40))

        self.verticalLayout_5.addWidget(self.PbAboutPage)


        self.horizontalLayout_15.addWidget(self.FMenuBtns, 0, Qt.AlignTop)


        self.horizontalLayout_13.addWidget(self.FMenuBar)

        self.SwSettings = QStackedWidget(self.FTabMenu)
        self.SwSettings.setObjectName(u"SwSettings")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SwSettings.sizePolicy().hasHeightForWidth())
        self.SwSettings.setSizePolicy(sizePolicy2)
        self.DownloadSettings = QWidget()
        self.DownloadSettings.setObjectName(u"DownloadSettings")
        self.verticalLayout_2 = QVBoxLayout(self.DownloadSettings)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.SaDownloadSettings = QScrollArea(self.DownloadSettings)
        self.SaDownloadSettings.setObjectName(u"SaDownloadSettings")
        self.SaDownloadSettings.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -89, 369, 275))
        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_10.setSpacing(15)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 15, 15, 0)
        self.FDownloadFolder = QFrame(self.scrollAreaWidgetContents)
        self.FDownloadFolder.setObjectName(u"FDownloadFolder")
        self.FDownloadFolder.setMinimumSize(QSize(0, 40))
        self.FDownloadFolder.setMaximumSize(QSize(16777215, 40))
        self.FDownloadFolder.setFrameShape(QFrame.StyledPanel)
        self.FDownloadFolder.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.FDownloadFolder)
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.LDownloadFolder = QLabel(self.FDownloadFolder)
        self.LDownloadFolder.setObjectName(u"LDownloadFolder")
        self.LDownloadFolder.setMinimumSize(QSize(100, 0))
        self.LDownloadFolder.setMaximumSize(QSize(100, 16777215))
        self.LDownloadFolder.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.LDownloadFolder)

        self.LeDownloadFolder = QLineEdit(self.FDownloadFolder)
        self.LeDownloadFolder.setObjectName(u"LeDownloadFolder")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.LeDownloadFolder.sizePolicy().hasHeightForWidth())
        self.LeDownloadFolder.setSizePolicy(sizePolicy3)
        self.LeDownloadFolder.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_8.addWidget(self.LeDownloadFolder)

        self.PbSelect = QPushButton(self.FDownloadFolder)
        self.PbSelect.setObjectName(u"PbSelect")
        self.PbSelect.setMinimumSize(QSize(40, 40))
        self.PbSelect.setIconSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.PbSelect)


        self.verticalLayout_10.addWidget(self.FDownloadFolder)

        self.FMaxThread = QFrame(self.scrollAreaWidgetContents)
        self.FMaxThread.setObjectName(u"FMaxThread")
        self.FMaxThread.setMinimumSize(QSize(0, 40))
        self.FMaxThread.setMaximumSize(QSize(16777215, 40))
        self.FMaxThread.setFrameShape(QFrame.StyledPanel)
        self.FMaxThread.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.FMaxThread)
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.LMaxThread = QLabel(self.FMaxThread)
        self.LMaxThread.setObjectName(u"LMaxThread")
        self.LMaxThread.setMinimumSize(QSize(100, 0))
        self.LMaxThread.setMaximumSize(QSize(100, 16777215))
        self.LMaxThread.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.LMaxThread)

        self.SbMaxThread = QSpinBox(self.FMaxThread)
        self.SbMaxThread.setObjectName(u"SbMaxThread")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SbMaxThread.sizePolicy().hasHeightForWidth())
        self.SbMaxThread.setSizePolicy(sizePolicy4)
        self.SbMaxThread.setMaximumSize(QSize(16777215, 40))
        self.SbMaxThread.setWrapping(False)
        self.SbMaxThread.setAlignment(Qt.AlignCenter)
        self.SbMaxThread.setMinimum(1)
        self.SbMaxThread.setMaximum(5)
        self.SbMaxThread.setSingleStep(1)
        self.SbMaxThread.setValue(1)

        self.horizontalLayout_9.addWidget(self.SbMaxThread)


        self.verticalLayout_10.addWidget(self.FMaxThread)

        self.FSleepTime = QFrame(self.scrollAreaWidgetContents)
        self.FSleepTime.setObjectName(u"FSleepTime")
        self.FSleepTime.setMinimumSize(QSize(0, 40))
        self.FSleepTime.setMaximumSize(QSize(16777215, 40))
        self.FSleepTime.setFrameShape(QFrame.StyledPanel)
        self.FSleepTime.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.FSleepTime)
        self.horizontalLayout_11.setSpacing(10)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.LSleepTime = QLabel(self.FSleepTime)
        self.LSleepTime.setObjectName(u"LSleepTime")
        self.LSleepTime.setMinimumSize(QSize(100, 0))
        self.LSleepTime.setMaximumSize(QSize(100, 16777215))
        self.LSleepTime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.LSleepTime)

        self.SbSleepTime = QSpinBox(self.FSleepTime)
        self.SbSleepTime.setObjectName(u"SbSleepTime")
        sizePolicy4.setHeightForWidth(self.SbSleepTime.sizePolicy().hasHeightForWidth())
        self.SbSleepTime.setSizePolicy(sizePolicy4)
        self.SbSleepTime.setMaximumSize(QSize(16777215, 40))
        self.SbSleepTime.setWrapping(False)
        self.SbSleepTime.setAlignment(Qt.AlignCenter)
        self.SbSleepTime.setMinimum(0)
        self.SbSleepTime.setMaximum(5000)
        self.SbSleepTime.setSingleStep(100)
        self.SbSleepTime.setValue(1000)

        self.horizontalLayout_11.addWidget(self.SbSleepTime)


        self.verticalLayout_10.addWidget(self.FSleepTime)

        self.FPathFormat = QFrame(self.scrollAreaWidgetContents)
        self.FPathFormat.setObjectName(u"FPathFormat")
        self.FPathFormat.setMinimumSize(QSize(0, 40))
        self.FPathFormat.setMaximumSize(QSize(16777215, 40))
        self.FPathFormat.setFrameShape(QFrame.StyledPanel)
        self.FPathFormat.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.FPathFormat)
        self.horizontalLayout_18.setSpacing(10)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.LPathFormat = QLabel(self.FPathFormat)
        self.LPathFormat.setObjectName(u"LPathFormat")
        self.LPathFormat.setMinimumSize(QSize(100, 0))
        self.LPathFormat.setMaximumSize(QSize(100, 16777215))
        self.LPathFormat.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.LPathFormat)

        self.LePathFormat = QLineEdit(self.FPathFormat)
        self.LePathFormat.setObjectName(u"LePathFormat")
        self.LePathFormat.setMinimumSize(QSize(0, 40))
        self.LePathFormat.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_18.addWidget(self.LePathFormat)


        self.verticalLayout_10.addWidget(self.FPathFormat)

        self.FTokutenPathFormat = QFrame(self.scrollAreaWidgetContents)
        self.FTokutenPathFormat.setObjectName(u"FTokutenPathFormat")
        self.FTokutenPathFormat.setMinimumSize(QSize(0, 40))
        self.FTokutenPathFormat.setMaximumSize(QSize(16777215, 40))
        self.FTokutenPathFormat.setFrameShape(QFrame.StyledPanel)
        self.FTokutenPathFormat.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.FTokutenPathFormat)
        self.horizontalLayout_17.setSpacing(10)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.LTokutenPathFormat = QLabel(self.FTokutenPathFormat)
        self.LTokutenPathFormat.setObjectName(u"LTokutenPathFormat")
        self.LTokutenPathFormat.setMinimumSize(QSize(100, 0))
        self.LTokutenPathFormat.setMaximumSize(QSize(100, 16777215))
        self.LTokutenPathFormat.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.LTokutenPathFormat)

        self.LeTokutenPathFormat = QLineEdit(self.FTokutenPathFormat)
        self.LeTokutenPathFormat.setObjectName(u"LeTokutenPathFormat")
        self.LeTokutenPathFormat.setMinimumSize(QSize(0, 40))
        self.LeTokutenPathFormat.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_17.addWidget(self.LeTokutenPathFormat)


        self.verticalLayout_10.addWidget(self.FTokutenPathFormat)

        self.SaDownloadSettings.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.SaDownloadSettings)

        self.SwSettings.addWidget(self.DownloadSettings)
        self.About = QWidget()
        self.About.setObjectName(u"About")
        self.horizontalLayout_12 = QHBoxLayout(self.About)
        self.horizontalLayout_12.setSpacing(15)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.FAbout = QFrame(self.About)
        self.FAbout.setObjectName(u"FAbout")
        self.FAbout.setFrameShape(QFrame.StyledPanel)
        self.FAbout.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.FAbout)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.FAppLogo = QFrame(self.FAbout)
        self.FAppLogo.setObjectName(u"FAppLogo")
        self.FAppLogo.setFrameShape(QFrame.StyledPanel)
        self.FAppLogo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.FAppLogo)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.LIconAbout = QLabel(self.FAppLogo)
        self.LIconAbout.setObjectName(u"LIconAbout")
        self.LIconAbout.setMinimumSize(QSize(64, 64))
        self.LIconAbout.setMaximumSize(QSize(64, 64))
        self.LIconAbout.setScaledContents(True)

        self.verticalLayout_9.addWidget(self.LIconAbout)


        self.verticalLayout_7.addWidget(self.FAppLogo, 0, Qt.AlignHCenter)

        self.FAppInfo = QFrame(self.FAbout)
        self.FAppInfo.setObjectName(u"FAppInfo")
        self.FAppInfo.setFrameShape(QFrame.StyledPanel)
        self.FAppInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.FAppInfo)
        self.verticalLayout_8.setSpacing(15)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.LAppName = QLabel(self.FAppInfo)
        self.LAppName.setObjectName(u"LAppName")
        self.LAppName.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.LAppName)

        self.LVersion = QLabel(self.FAppInfo)
        self.LVersion.setObjectName(u"LVersion")
        self.LVersion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.LVersion)

        self.LGithub = QLabel(self.FAppInfo)
        self.LGithub.setObjectName(u"LGithub")
        self.LGithub.setTextFormat(Qt.RichText)
        self.LGithub.setAlignment(Qt.AlignCenter)
        self.LGithub.setOpenExternalLinks(True)

        self.verticalLayout_8.addWidget(self.LGithub)


        self.verticalLayout_7.addWidget(self.FAppInfo)


        self.horizontalLayout_12.addWidget(self.FAbout)

        self.SwSettings.addWidget(self.About)
        self.SpiderSettings = QWidget()
        self.SpiderSettings.setObjectName(u"SpiderSettings")
        self.verticalLayout_3 = QVBoxLayout(self.SpiderSettings)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.FCookie = QFrame(self.SpiderSettings)
        self.FCookie.setObjectName(u"FCookie")
        self.FCookie.setMinimumSize(QSize(0, 40))
        self.FCookie.setMaximumSize(QSize(16777215, 40))
        self.FCookie.setFrameShape(QFrame.StyledPanel)
        self.FCookie.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.FCookie)
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.LCookie = QLabel(self.FCookie)
        self.LCookie.setObjectName(u"LCookie")
        self.LCookie.setMinimumSize(QSize(100, 0))
        self.LCookie.setMaximumSize(QSize(100, 16777215))
        self.LCookie.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.LCookie)

        self.LeCookie = QLineEdit(self.FCookie)
        self.LeCookie.setObjectName(u"LeCookie")
        sizePolicy3.setHeightForWidth(self.LeCookie.sizePolicy().hasHeightForWidth())
        self.LeCookie.setSizePolicy(sizePolicy3)
        self.LeCookie.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_6.addWidget(self.LeCookie)

        self.PbLogin = QPushButton(self.FCookie)
        self.PbLogin.setObjectName(u"PbLogin")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.PbLogin.sizePolicy().hasHeightForWidth())
        self.PbLogin.setSizePolicy(sizePolicy5)
        self.PbLogin.setMinimumSize(QSize(80, 40))

        self.horizontalLayout_6.addWidget(self.PbLogin)


        self.verticalLayout_3.addWidget(self.FCookie)

        self.FProxy = QFrame(self.SpiderSettings)
        self.FProxy.setObjectName(u"FProxy")
        self.FProxy.setMinimumSize(QSize(0, 40))
        self.FProxy.setMaximumSize(QSize(16777215, 40))
        self.FProxy.setFrameShape(QFrame.StyledPanel)
        self.FProxy.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.FProxy)
        self.horizontalLayout_7.setSpacing(10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.LProxy = QLabel(self.FProxy)
        self.LProxy.setObjectName(u"LProxy")
        self.LProxy.setMinimumSize(QSize(100, 0))
        self.LProxy.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_7.addWidget(self.LProxy)

        self.LeProxy = QLineEdit(self.FProxy)
        self.LeProxy.setObjectName(u"LeProxy")
        sizePolicy3.setHeightForWidth(self.LeProxy.sizePolicy().hasHeightForWidth())
        self.LeProxy.setSizePolicy(sizePolicy3)
        self.LeProxy.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_7.addWidget(self.LeProxy)


        self.verticalLayout_3.addWidget(self.FProxy)

        self.SwSettings.addWidget(self.SpiderSettings)
        self.GeneralSettings = QWidget()
        self.GeneralSettings.setObjectName(u"GeneralSettings")
        self.verticalLayout_6 = QVBoxLayout(self.GeneralSettings)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.FCheckUpdateStart = QFrame(self.GeneralSettings)
        self.FCheckUpdateStart.setObjectName(u"FCheckUpdateStart")
        self.FCheckUpdateStart.setMinimumSize(QSize(0, 40))
        self.FCheckUpdateStart.setMaximumSize(QSize(16777215, 40))
        self.FCheckUpdateStart.setFrameShape(QFrame.StyledPanel)
        self.FCheckUpdateStart.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.FCheckUpdateStart)
        self.horizontalLayout_10.setSpacing(10)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.LCheckUpdateStart = QLabel(self.FCheckUpdateStart)
        self.LCheckUpdateStart.setObjectName(u"LCheckUpdateStart")
        self.LCheckUpdateStart.setMinimumSize(QSize(100, 0))
        self.LCheckUpdateStart.setMaximumSize(QSize(100, 16777215))
        self.LCheckUpdateStart.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.LCheckUpdateStart)

        self.CbCheckUpdateStart = QCheckBox(self.FCheckUpdateStart)
        self.CbCheckUpdateStart.setObjectName(u"CbCheckUpdateStart")
        sizePolicy4.setHeightForWidth(self.CbCheckUpdateStart.sizePolicy().hasHeightForWidth())
        self.CbCheckUpdateStart.setSizePolicy(sizePolicy4)
        self.CbCheckUpdateStart.setMaximumSize(QSize(16777215, 40))
        self.CbCheckUpdateStart.setChecked(True)

        self.horizontalLayout_10.addWidget(self.CbCheckUpdateStart)

        self.PbCheckUpdate = QPushButton(self.FCheckUpdateStart)
        self.PbCheckUpdate.setObjectName(u"PbCheckUpdate")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.PbCheckUpdate.sizePolicy().hasHeightForWidth())
        self.PbCheckUpdate.setSizePolicy(sizePolicy6)
        self.PbCheckUpdate.setMinimumSize(QSize(0, 40))
        self.PbCheckUpdate.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_10.addWidget(self.PbCheckUpdate)


        self.verticalLayout_6.addWidget(self.FCheckUpdateStart)

        self.FStyle = QFrame(self.GeneralSettings)
        self.FStyle.setObjectName(u"FStyle")
        self.FStyle.setMinimumSize(QSize(0, 40))
        self.FStyle.setMaximumSize(QSize(16777215, 40))
        self.FStyle.setFrameShape(QFrame.StyledPanel)
        self.FStyle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.FStyle)
        self.horizontalLayout_16.setSpacing(10)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.LStyle = QLabel(self.FStyle)
        self.LStyle.setObjectName(u"LStyle")
        self.LStyle.setMinimumSize(QSize(100, 0))
        self.LStyle.setMaximumSize(QSize(100, 16777215))
        self.LStyle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.LStyle)

        self.CbStyle = QComboBox(self.FStyle)
        self.CbStyle.setObjectName(u"CbStyle")
        self.CbStyle.setMinimumSize(QSize(0, 40))
        self.CbStyle.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_16.addWidget(self.CbStyle)


        self.verticalLayout_6.addWidget(self.FStyle)

        self.SwSettings.addWidget(self.GeneralSettings)

        self.horizontalLayout_13.addWidget(self.SwSettings, 0, Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.FTabMenu)

        self.FSubmit = QFrame(self.FContentBar)
        self.FSubmit.setObjectName(u"FSubmit")
        self.FSubmit.setMinimumSize(QSize(0, 50))
        self.FSubmit.setMaximumSize(QSize(16777215, 50))
        self.FSubmit.setFrameShape(QFrame.StyledPanel)
        self.FSubmit.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.FSubmit)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.PbSubmit = QPushButton(self.FSubmit)
        self.PbSubmit.setObjectName(u"PbSubmit")
        sizePolicy3.setHeightForWidth(self.PbSubmit.sizePolicy().hasHeightForWidth())
        self.PbSubmit.setSizePolicy(sizePolicy3)
        self.PbSubmit.setMinimumSize(QSize(0, 30))
        self.PbSubmit.setMaximumSize(QSize(300, 50))

        self.horizontalLayout_14.addWidget(self.PbSubmit)


        self.verticalLayout_4.addWidget(self.FSubmit)


        self.verticalLayout.addWidget(self.FContentBar, 0, Qt.AlignHCenter)

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

        self.SwSettings.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LIcon.setText("")
        self.LTitle.setText("")
        self.PbMinimize.setText("")
        self.PbClose.setText("")
        self.PbDownloadPage.setText("")
        self.PbSpiderPage.setText("")
        self.PbGeneralPage.setText("")
        self.PbAboutPage.setText("")
        self.LDownloadFolder.setText("")
        self.PbSelect.setText("")
        self.LMaxThread.setText("")
        self.SbMaxThread.setSuffix("")
        self.SbMaxThread.setPrefix("")
        self.LSleepTime.setText("")
        self.SbSleepTime.setSuffix(QCoreApplication.translate("MainWindow", u"\u6beb\u79d2", None))
        self.SbSleepTime.setPrefix("")
        self.LPathFormat.setText("")
        self.LTokutenPathFormat.setText("")
        self.LIconAbout.setText("")
        self.LAppName.setText("")
        self.LVersion.setText("")
        self.LGithub.setText("")
        self.LCookie.setText("")
        self.PbLogin.setText("")
        self.LProxy.setText("")
        self.LCheckUpdateStart.setText("")
        self.CbCheckUpdateStart.setText("")
        self.PbCheckUpdate.setText("")
        self.LStyle.setText("")
        self.PbSubmit.setText("")
        self.LStatus.setText("")
    # retranslateUi

