# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'template.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import sources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(665, 539)
        MainWindow.setMinimumSize(QSize(400, 270))
        MainWindow.setMouseTracking(True)
        icon = QIcon()
        icon.addFile(u":/imgs/imgs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMouseTracking(True)
        self.margin_layout = QVBoxLayout(self.centralwidget)
        self.margin_layout.setSpacing(0)
        self.margin_layout.setObjectName(u"margin_layout")
        self.margin_layout.setContentsMargins(0, 0, 0, 0)
        self.background = QWidget(self.centralwidget)
        self.background.setObjectName(u"background")
        self.background.setMouseTracking(True)
        self.background.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.background)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title_bar = QFrame(self.background)
        self.title_bar.setObjectName(u"title_bar")
        self.title_bar.setMaximumSize(QSize(16777215, 35))
        self.title_bar.setMouseTracking(True)
        self.title_bar.setFrameShape(QFrame.NoFrame)
        self.title_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.title_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.title_box = QFrame(self.title_bar)
        self.title_box.setObjectName(u"title_box")
        self.title_box.setMouseTracking(True)
        self.title_box.setFrameShape(QFrame.StyledPanel)
        self.title_box.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.title_box)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.icon_box = QFrame(self.title_box)
        self.icon_box.setObjectName(u"icon_box")
        self.icon_box.setMaximumSize(QSize(35, 35))
        self.icon_box.setMouseTracking(True)
        self.icon_box.setStyleSheet(u"")
        self.icon_box.setFrameShape(QFrame.StyledPanel)
        self.icon_box.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.icon_box)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.icon_label = QLabel(self.icon_box)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMouseTracking(True)
        self.icon_label.setPixmap(QPixmap(u":/imgs/imgs/icon.png"))
        self.icon_label.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.icon_label)


        self.horizontalLayout_3.addWidget(self.icon_box)

        self.title_label_box = QFrame(self.title_box)
        self.title_label_box.setObjectName(u"title_label_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label_box.sizePolicy().hasHeightForWidth())
        self.title_label_box.setSizePolicy(sizePolicy)
        self.title_label_box.setMouseTracking(True)
        self.title_label_box.setFrameShape(QFrame.StyledPanel)
        self.title_label_box.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.title_label_box)
        self.horizontalLayout_7.setSpacing(3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.title_label_box)
        self.label.setObjectName(u"label")
        self.label.setMouseTracking(True)
        self.label.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.title_label_box)


        self.horizontalLayout.addWidget(self.title_box)

        self.title_btns_box = QFrame(self.title_bar)
        self.title_btns_box.setObjectName(u"title_btns_box")
        self.title_btns_box.setMaximumSize(QSize(170, 16777215))
        self.title_btns_box.setMouseTracking(True)
        self.title_btns_box.setFrameShape(QFrame.StyledPanel)
        self.title_btns_box.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.title_btns_box)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_min = QPushButton(self.title_btns_box)
        self.btn_min.setObjectName(u"btn_min")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_min.sizePolicy().hasHeightForWidth())
        self.btn_min.setSizePolicy(sizePolicy1)
        self.btn_min.setMouseTracking(True)
        self.btn_min.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/imgs/imgs/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_min.setIcon(icon1)
        self.btn_min.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.btn_min)

        self.btn_max = QPushButton(self.title_btns_box)
        self.btn_max.setObjectName(u"btn_max")
        sizePolicy1.setHeightForWidth(self.btn_max.sizePolicy().hasHeightForWidth())
        self.btn_max.setSizePolicy(sizePolicy1)
        self.btn_max.setMouseTracking(True)
        self.btn_max.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/imgs/imgs/maximum.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_max.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btn_max)

        self.btn_close = QPushButton(self.title_btns_box)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMouseTracking(True)
        self.btn_close.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/imgs/imgs/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.btn_close)


        self.horizontalLayout.addWidget(self.title_btns_box)


        self.verticalLayout.addWidget(self.title_bar)

        self.content_bar = QFrame(self.background)
        self.content_bar.setObjectName(u"content_bar")
        self.content_bar.setMouseTracking(True)
        self.content_bar.setFrameShape(QFrame.NoFrame)
        self.content_bar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.content_bar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.manga_input = QFrame(self.content_bar)
        self.manga_input.setObjectName(u"manga_input")
        self.manga_input.setMaximumSize(QSize(16777215, 100))
        self.manga_input.setMouseTracking(True)
        self.manga_input.setFrameShape(QFrame.StyledPanel)
        self.manga_input.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.manga_input)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.input_sets = QFrame(self.manga_input)
        self.input_sets.setObjectName(u"input_sets")
        self.input_sets.setMouseTracking(True)
        self.input_sets.setFrameShape(QFrame.StyledPanel)
        self.input_sets.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.input_sets)
        self.horizontalLayout_8.setSpacing(9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(9, 0, 9, 0)
        self.website_label = QLabel(self.input_sets)
        self.website_label.setObjectName(u"website_label")
        self.website_label.setMinimumSize(QSize(0, 0))
        self.website_label.setMouseTracking(True)
        self.website_label.setStyleSheet(u"")

        self.horizontalLayout_8.addWidget(self.website_label)

        self.website_input = QLineEdit(self.input_sets)
        self.website_input.setObjectName(u"website_input")
        self.website_input.setMinimumSize(QSize(0, 32))
        self.website_input.setMaximumSize(QSize(16777215, 32))
        self.website_input.setMouseTracking(True)
        self.website_input.setStyleSheet(u"")

        self.horizontalLayout_8.addWidget(self.website_input)

        self.btn_getinfo = QPushButton(self.input_sets)
        self.btn_getinfo.setObjectName(u"btn_getinfo")
        sizePolicy1.setHeightForWidth(self.btn_getinfo.sizePolicy().hasHeightForWidth())
        self.btn_getinfo.setSizePolicy(sizePolicy1)
        self.btn_getinfo.setMinimumSize(QSize(150, 32))
        self.btn_getinfo.setMaximumSize(QSize(16777215, 32))
        self.btn_getinfo.setMouseTracking(True)
        self.btn_getinfo.setStyleSheet(u"")
        self.btn_getinfo.setFlat(False)

        self.horizontalLayout_8.addWidget(self.btn_getinfo)


        self.verticalLayout_3.addWidget(self.input_sets)

        self.frame = QFrame(self.manga_input)
        self.frame.setObjectName(u"frame")
        self.frame.setMouseTracking(True)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tips_label = QLabel(self.frame)
        self.tips_label.setObjectName(u"tips_label")
        self.tips_label.setMouseTracking(True)
        self.tips_label.setStyleSheet(u"")
        self.tips_label.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.tips_label)


        self.verticalLayout_3.addWidget(self.frame)


        self.verticalLayout_2.addWidget(self.manga_input)

        self.manga_detail = QFrame(self.content_bar)
        self.manga_detail.setObjectName(u"manga_detail")
        self.manga_detail.setMouseTracking(True)
        self.manga_detail.setFrameShape(QFrame.StyledPanel)
        self.manga_detail.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.manga_detail)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 0, -1, 0)
        self.title_and_author = QFrame(self.manga_detail)
        self.title_and_author.setObjectName(u"title_and_author")
        self.title_and_author.setMouseTracking(True)
        self.title_and_author.setFrameShape(QFrame.StyledPanel)
        self.title_and_author.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.title_and_author)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.title = QFrame(self.title_and_author)
        self.title.setObjectName(u"title")
        self.title.setMouseTracking(True)
        self.title.setFrameShape(QFrame.StyledPanel)
        self.title.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.title)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(50, 16777215))
        self.title_label.setMouseTracking(True)
        self.title_label.setStyleSheet(u"")

        self.horizontalLayout_10.addWidget(self.title_label)

        self.manga_title = QLabel(self.title)
        self.manga_title.setObjectName(u"manga_title")
        self.manga_title.setMouseTracking(True)
        self.manga_title.setStyleSheet(u"")
        self.manga_title.setWordWrap(True)

        self.horizontalLayout_10.addWidget(self.manga_title)


        self.horizontalLayout_11.addWidget(self.title)

        self.author = QFrame(self.title_and_author)
        self.author.setObjectName(u"author")
        self.author.setMouseTracking(True)
        self.author.setFrameShape(QFrame.StyledPanel)
        self.author.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.author)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.author_label = QLabel(self.author)
        self.author_label.setObjectName(u"author_label")
        self.author_label.setMaximumSize(QSize(50, 16777215))
        self.author_label.setMouseTracking(True)
        self.author_label.setStyleSheet(u"")

        self.horizontalLayout_9.addWidget(self.author_label)

        self.manga_author = QLabel(self.author)
        self.manga_author.setObjectName(u"manga_author")
        self.manga_author.setMouseTracking(True)
        self.manga_author.setStyleSheet(u"")
        self.manga_author.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.manga_author)


        self.horizontalLayout_11.addWidget(self.author)


        self.verticalLayout_6.addWidget(self.title_and_author)

        self.description = QFrame(self.manga_detail)
        self.description.setObjectName(u"description")
        self.description.setMouseTracking(True)
        self.description.setFrameShape(QFrame.StyledPanel)
        self.description.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.description)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.description_label = QLabel(self.description)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setMaximumSize(QSize(50, 16777215))
        self.description_label.setMouseTracking(True)
        self.description_label.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.description_label)

        self.manga_description = QLabel(self.description)
        self.manga_description.setObjectName(u"manga_description")
        self.manga_description.setMouseTracking(True)
        self.manga_description.setStyleSheet(u"")
        self.manga_description.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.manga_description)


        self.verticalLayout_6.addWidget(self.description)

        self.manga_list = QFrame(self.manga_detail)
        self.manga_list.setObjectName(u"manga_list")
        self.manga_list.setMouseTracking(True)
        self.manga_list.setFrameShape(QFrame.StyledPanel)
        self.manga_list.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.manga_list)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.list_label = QLabel(self.manga_list)
        self.list_label.setObjectName(u"list_label")
        self.list_label.setMaximumSize(QSize(50, 16777215))
        self.list_label.setMouseTracking(True)
        self.list_label.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.list_label)

        self.listWidget = QListWidget(self.manga_list)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMouseTracking(True)
        self.listWidget.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.listWidget)


        self.verticalLayout_6.addWidget(self.manga_list)


        self.verticalLayout_2.addWidget(self.manga_detail)

        self.user_operate = QFrame(self.content_bar)
        self.user_operate.setObjectName(u"user_operate")
        self.user_operate.setMouseTracking(True)
        self.user_operate.setFrameShape(QFrame.StyledPanel)
        self.user_operate.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.user_operate)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.btn_startdownload = QPushButton(self.user_operate)
        self.btn_startdownload.setObjectName(u"btn_startdownload")
        sizePolicy1.setHeightForWidth(self.btn_startdownload.sizePolicy().hasHeightForWidth())
        self.btn_startdownload.setSizePolicy(sizePolicy1)
        self.btn_startdownload.setMinimumSize(QSize(100, 32))
        self.btn_startdownload.setMaximumSize(QSize(16777215, 32))
        self.btn_startdownload.setMouseTracking(True)
        self.btn_startdownload.setStyleSheet(u"")
        self.btn_startdownload.setFlat(False)

        self.horizontalLayout_12.addWidget(self.btn_startdownload)

        self.progressBar = QProgressBar(self.user_operate)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 32))
        self.progressBar.setMouseTracking(True)
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout_12.addWidget(self.progressBar)

        self.btn_selectall = QPushButton(self.user_operate)
        self.btn_selectall.setObjectName(u"btn_selectall")
        sizePolicy1.setHeightForWidth(self.btn_selectall.sizePolicy().hasHeightForWidth())
        self.btn_selectall.setSizePolicy(sizePolicy1)
        self.btn_selectall.setMinimumSize(QSize(50, 32))
        self.btn_selectall.setMaximumSize(QSize(16777215, 32))
        self.btn_selectall.setMouseTracking(True)
        self.btn_selectall.setStyleSheet(u"")
        self.btn_selectall.setFlat(False)

        self.horizontalLayout_12.addWidget(self.btn_selectall)

        self.btn_cancelall = QPushButton(self.user_operate)
        self.btn_cancelall.setObjectName(u"btn_cancelall")
        sizePolicy1.setHeightForWidth(self.btn_cancelall.sizePolicy().hasHeightForWidth())
        self.btn_cancelall.setSizePolicy(sizePolicy1)
        self.btn_cancelall.setMinimumSize(QSize(50, 32))
        self.btn_cancelall.setMaximumSize(QSize(16777215, 32))
        self.btn_cancelall.setMouseTracking(True)
        self.btn_cancelall.setStyleSheet(u"")
        self.btn_cancelall.setFlat(False)

        self.horizontalLayout_12.addWidget(self.btn_cancelall)

        self.btn_moresettings = QPushButton(self.user_operate)
        self.btn_moresettings.setObjectName(u"btn_moresettings")
        sizePolicy1.setHeightForWidth(self.btn_moresettings.sizePolicy().hasHeightForWidth())
        self.btn_moresettings.setSizePolicy(sizePolicy1)
        self.btn_moresettings.setMinimumSize(QSize(100, 32))
        self.btn_moresettings.setMaximumSize(QSize(16777215, 32))
        self.btn_moresettings.setMouseTracking(True)
        self.btn_moresettings.setStyleSheet(u"")
        self.btn_moresettings.setFlat(False)

        self.horizontalLayout_12.addWidget(self.btn_moresettings)


        self.verticalLayout_2.addWidget(self.user_operate)


        self.verticalLayout.addWidget(self.content_bar)

        self.status_bar = QFrame(self.background)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setMaximumSize(QSize(16777215, 25))
        self.status_bar.setMouseTracking(True)
        self.status_bar.setFrameShape(QFrame.NoFrame)
        self.status_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.status_bar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.copyright = QLabel(self.status_bar)
        self.copyright.setObjectName(u"copyright")
        self.copyright.setMouseTracking(True)
        self.copyright.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.copyright)


        self.verticalLayout.addWidget(self.status_bar)


        self.margin_layout.addWidget(self.background)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bilibili Manga Downloader V1.0.0", None))
        self.icon_label.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u54d4\u54e9\u54d4\u54e9\u6f2b\u753b\u4e0b\u8f7d\u5668 V1.0.0 - \u5c1a\u672a\u8bbe\u7f6ecookie", None))
        self.btn_min.setText("")
        self.btn_max.setText("")
        self.btn_close.setText("")
        self.website_label.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753b\u7f51\u5740", None))
#if QT_CONFIG(statustip)
        self.website_input.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.website_input.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.website_input.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.website_input.setPlaceholderText("")
        self.btn_getinfo.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u6f2b\u753b\u4fe1\u606f", None))
        self.tips_label.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u793a\uff1a\u4ec5\u652f\u6301\u54d4\u54e9\u54d4\u54e9\u6f2b\u753b\uff0c\u4f8b\u5982https://manga.bilibili.com/detail/mc28528", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753b\u6807\u9898", None))
        self.manga_title.setText(QCoreApplication.translate("MainWindow", u"\u6682\u65e0", None))
        self.author_label.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753b\u4f5c\u8005", None))
        self.manga_author.setText(QCoreApplication.translate("MainWindow", u"\u6682\u65e0", None))
        self.description_label.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753b\u63cf\u8ff0", None))
        self.manga_description.setText(QCoreApplication.translate("MainWindow", u"\u6682\u65e0", None))
        self.list_label.setText(QCoreApplication.translate("MainWindow", u"\u7ae0\u8282\u5217\u8868", None))
        self.btn_startdownload.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.btn_selectall.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
        self.btn_cancelall.setText(QCoreApplication.translate("MainWindow", u"\u5168\u4e0d\u9009", None))
        self.btn_moresettings.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u591a\u8bbe\u7f6e", None))
        self.copyright.setText(QCoreApplication.translate("MainWindow", u"Developed by Tao Ye. 2022\u00a9All Rights Reserved.", None))
    # retranslateUi

