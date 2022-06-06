from frameless_window import WindowsFramelessWindow
from downloader_login_web_base_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Signal
import sys
import core


class LoginWebWindow(WindowsFramelessWindow):
    cookieSignal = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cookie = {}

        # set style sheet
        self.setStyleSheet(core.QSS)

        # set ui text
        self.ui.LTitle.setText('登录B站账号')
        self.setWindowTitle('登录B站账号')
        self.ui.LInstructions.setText('请在下方的网页中点击右上角的“登录”按钮进行登录，成功后关闭窗口即可。')

        # set ui icons
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])

        # connect signals
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)
        self.ui.PbClose.clicked.connect(self.close)

        self.webEngine = QWebEngineView(self.ui.FWebPage)
        self.ui.horizontalLayout_7.addWidget(self.webEngine)
        self.webEngine.page().profile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.webEngine.load(QUrl("https://manga.bilibili.com/"))

    def onCookieAdd(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookie[name] = value

    def closeEvent(self, event) -> None:
        self.cookieSignal.emit(self.cookie)
        return super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    core.read_config_file()
    core.load_qss()
    core.load_resource()
    widget = LoginWebWindow()
    widget.show()
    sys.exit(app.exec())
