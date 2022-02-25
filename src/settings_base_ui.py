# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(550, 295)
        icon = QIcon()
        icon.addFile(u"imgs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"")
        self.margin_layout = QVBoxLayout(Form)
        self.margin_layout.setSpacing(0)
        self.margin_layout.setObjectName(u"margin_layout")
        self.margin_layout.setContentsMargins(0, 0, 0, 0)
        self.background = QWidget(Form)
        self.background.setObjectName(u"background")
        self.background.setStyleSheet(u"background-color:#1f2430")
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
        self.icon_label.setPixmap(QPixmap(u"imgs/icon.png"))
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
        self.label.setStyleSheet(u"color:#cccac2")

        self.horizontalLayout_7.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.title_label_box)


        self.horizontalLayout.addWidget(self.title_box)

        self.title_btns_box = QFrame(self.title_bar)
        self.title_btns_box.setObjectName(u"title_btns_box")
        self.title_btns_box.setMaximumSize(QSize(100, 16777215))
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
        self.btn_min.setStyleSheet(u"QPushButton{border:none}\n"
"QPushButton:hover{background-color:#363a45}")
        icon1 = QIcon()
        icon1.addFile(u"imgs/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_min.setIcon(icon1)
        self.btn_min.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.btn_min)

        self.btn_close = QPushButton(self.title_btns_box)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMouseTracking(True)
        self.btn_close.setStyleSheet(u"QPushButton{border:none}\n"
"QPushButton:hover{background-color:#d41325}")
        icon2 = QIcon()
        icon2.addFile(u"imgs/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btn_close)


        self.horizontalLayout.addWidget(self.title_btns_box)


        self.verticalLayout.addWidget(self.title_bar)

        self.content_bar = QFrame(self.background)
        self.content_bar.setObjectName(u"content_bar")
        self.content_bar.setMouseTracking(True)
        self.content_bar.setFrameShape(QFrame.NoFrame)
        self.content_bar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.content_bar)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.cookie_set = QFrame(self.content_bar)
        self.cookie_set.setObjectName(u"cookie_set")
        self.cookie_set.setFrameShape(QFrame.StyledPanel)
        self.cookie_set.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.cookie_set)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cookie_label = QLabel(self.cookie_set)
        self.cookie_label.setObjectName(u"cookie_label")
        self.cookie_label.setMinimumSize(QSize(50, 0))
        self.cookie_label.setMouseTracking(True)
        self.cookie_label.setStyleSheet(u"color:#cccac2")
        self.cookie_label.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.cookie_label)

        self.cookie_input = QLineEdit(self.cookie_set)
        self.cookie_input.setObjectName(u"cookie_input")
        self.cookie_input.setMinimumSize(QSize(0, 32))
        self.cookie_input.setMaximumSize(QSize(16777215, 32))
        self.cookie_input.setMouseTracking(True)
        self.cookie_input.setStyleSheet(u"QLineEdit{\n"
"	border:1px solid #383f4d;\n"
"	background-color:#242936;\n"
"	color:#cccac2\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"	border:1px solid #c4a25f;\n"
"}")

        self.horizontalLayout_4.addWidget(self.cookie_input)


        self.verticalLayout_2.addWidget(self.cookie_set)

        self.path_set = QFrame(self.content_bar)
        self.path_set.setObjectName(u"path_set")
        self.path_set.setFrameShape(QFrame.StyledPanel)
        self.path_set.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.path_set)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.path_label = QLabel(self.path_set)
        self.path_label.setObjectName(u"path_label")
        self.path_label.setMinimumSize(QSize(50, 0))
        self.path_label.setMouseTracking(True)
        self.path_label.setStyleSheet(u"color:#cccac2")
        self.path_label.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.path_label)

        self.path_input = QLineEdit(self.path_set)
        self.path_input.setObjectName(u"path_input")
        self.path_input.setMinimumSize(QSize(0, 32))
        self.path_input.setMaximumSize(QSize(16777215, 32))
        self.path_input.setMouseTracking(True)
        self.path_input.setStyleSheet(u"QLineEdit{\n"
"	border:1px solid #383f4d;\n"
"	background-color:#242936;\n"
"	color:#cccac2\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"	border:1px solid #c4a25f;\n"
"}")

        self.horizontalLayout_9.addWidget(self.path_input)

        self.btn_select = QPushButton(self.path_set)
        self.btn_select.setObjectName(u"btn_select")
        sizePolicy1.setHeightForWidth(self.btn_select.sizePolicy().hasHeightForWidth())
        self.btn_select.setSizePolicy(sizePolicy1)
        self.btn_select.setMinimumSize(QSize(32, 32))
        self.btn_select.setMaximumSize(QSize(32, 32))
        self.btn_select.setMouseTracking(True)
        self.btn_select.setStyleSheet(u"QPushButton{\n"
"background-color:#ffcc66;\n"
"color:#805500;\n"
"border-style:outset;\n"
"}")
        self.btn_select.setFlat(False)

        self.horizontalLayout_9.addWidget(self.btn_select)


        self.verticalLayout_2.addWidget(self.path_set)

        self.interval_set = QFrame(self.content_bar)
        self.interval_set.setObjectName(u"interval_set")
        self.interval_set.setFrameShape(QFrame.StyledPanel)
        self.interval_set.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.interval_set)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.interval_label = QLabel(self.interval_set)
        self.interval_label.setObjectName(u"interval_label")
        self.interval_label.setMinimumSize(QSize(50, 0))
        self.interval_label.setMouseTracking(True)
        self.interval_label.setStyleSheet(u"color:#cccac2")
        self.interval_label.setWordWrap(True)

        self.horizontalLayout_8.addWidget(self.interval_label)

        self.spinBox = QSpinBox(self.interval_set)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy2)
        self.spinBox.setMinimumSize(QSize(0, 32))
        self.spinBox.setStyleSheet(u"QSpinBox{\n"
"	border:1px solid #383f4d;\n"
"	background-color:#242936;\n"
"	color:#cccac2\n"
"}\n"
"\n"
"QSpinBox:focus{\n"
"	border:1px solid #c4a25f;\n"
"}\n"
"\n"
"QSpinBox::down-button{\n"
"    border-style:outset;\n"
"}\n"
"\n"
"QSpinBox::up-button{\n"
"    border-style:outset;\n"
"}")
        self.spinBox.setMaximum(5000)

        self.horizontalLayout_8.addWidget(self.spinBox)


        self.verticalLayout_2.addWidget(self.interval_set)


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
        self.copyright.setStyleSheet(u"color:#cccac2")

        self.horizontalLayout_5.addWidget(self.copyright)


        self.verticalLayout.addWidget(self.status_bar)


        self.margin_layout.addWidget(self.background)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Settings", None))
        self.icon_label.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u66f4\u591a\u8bbe\u7f6e - \u5173\u95ed\u7a97\u53e3\u4f7f\u8bbe\u7f6e\u751f\u6548", None))
        self.btn_min.setText("")
        self.btn_close.setText("")
        self.cookie_label.setText(QCoreApplication.translate("Form", u"cookie", None))
#if QT_CONFIG(statustip)
        self.cookie_input.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.cookie_input.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.cookie_input.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.cookie_input.setPlaceholderText("")
        self.path_label.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u8def\u5f84", None))
#if QT_CONFIG(statustip)
        self.path_input.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.path_input.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.path_input.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.path_input.setPlaceholderText("")
        self.btn_select.setText(QCoreApplication.translate("Form", u"...", None))
        self.interval_label.setText(QCoreApplication.translate("Form", u"\u95f4\u9694\u65f6\u957f", None))
        self.spinBox.setSuffix(QCoreApplication.translate("Form", u"\u6beb\u79d2", None))
        self.spinBox.setPrefix("")
        self.copyright.setText(QCoreApplication.translate("Form", u"Developed by Tao Ye. 2022\u00a9All Rights Reserved.", None))
    # retranslateUi

