import sys
import os
import json
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from frameless_window import WindowsFramelessWindow
from downloader_settings_base_ui import Ui_MainWindow
from check_update_thread import CheckUpdateThread
from downloader_login_web_ui import LoginWebWindow
import core
import service


class SettingsWindow(WindowsFramelessWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set style sheet
        self.setStyleSheet(core.QSS)

        self.ui.LeCookie.textChanged.connect(
            lambda: self.ui.LeCookie.style().polish(self.ui.LeCookie))
        self.ui.LeDownloadFolder.textChanged.connect(
            lambda: self.ui.LeDownloadFolder.style().polish(self.ui.LeDownloadFolder))
        self.ui.LeProxy.textChanged.connect(
            lambda: self.ui.LeProxy.style().polish(self.ui.LeProxy))
        self.ui.LePathFormat.textChanged.connect(
            lambda: self.ui.LePathFormat.style().polish(self.ui.LePathFormat))
        self.ui.LeTokutenPathFormat.textChanged.connect(
            lambda: self.ui.LeTokutenPathFormat.style().polish(self.ui.LeTokutenPathFormat))

        # set text
        self.ui.LTitle.setText('设置')
        self.setWindowTitle('设置')
        self.ui.LCookie.setText('账户Cookie')
        self.ui.LDownloadFolder.setText('下载根目录')
        self.ui.LMaxThread.setText('最大下载线程数')
        self.ui.LCheckUpdateStart.setText('启动时检查更新')
        self.ui.LSleepTime.setText('下载间隔时间')
        self.ui.PbSubmit.setText('保存设置')
        self.ui.PbLogin.setText('自动获取')
        self.ui.PbCheckUpdate.setText('检查更新')
        self.ui.LProxy.setText('设置HTTPS代理')
        self.ui.LAppName.setText('哔哩哔哩漫画下载器')
        self.ui.LVersion.setText(core.VERSION_TAG)
        self.ui.LStyle.setText('主题(重启生效)')
        self.ui.LPathFormat.setText('下载路径格式')
        self.ui.LTokutenPathFormat.setText('特典路径格式')
        self.ui.LGithub.setText(
            '<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/" style="text-decoration: none;color:#91ddff;">GitHub')

        for style in core.STYLE_CHOICE.values():
            self.ui.CbStyle.insertItem(0, style)
        self.ui.SwSettings.setCurrentIndex(0)
        self.ui.PbAboutPage.setText('关于')
        self.ui.PbAboutPage.setCheckable(True)
        self.ui.PbAboutPage.setAutoExclusive(True)
        self.ui.PbAboutPage.clicked.connect(
            lambda: self.ui.SwSettings.setCurrentIndex(1))
        self.ui.PbDownloadPage.setText('下载')
        self.ui.PbDownloadPage.setCheckable(True)
        self.ui.PbDownloadPage.setAutoExclusive(True)
        self.ui.PbDownloadPage.setChecked(True)
        self.ui.PbDownloadPage.clicked.connect(
            lambda: self.ui.SwSettings.setCurrentIndex(0))
        self.ui.PbGeneralPage.setText('通用')
        self.ui.PbGeneralPage.setCheckable(True)
        self.ui.PbGeneralPage.setAutoExclusive(True)
        self.ui.PbGeneralPage.clicked.connect(
            lambda: self.ui.SwSettings.setCurrentIndex(3))
        self.ui.PbSpiderPage.setText('爬虫')
        self.ui.PbSpiderPage.setCheckable(True)
        self.ui.PbSpiderPage.setAutoExclusive(True)
        self.ui.PbSpiderPage.clicked.connect(
            lambda: self.ui.SwSettings.setCurrentIndex(2))
        self.ui.CbStyle.setCurrentText(core.STYLE_CHOICE[core.CONFIG['style']])
        self.ui.LePathFormat.setText(core.CONFIG['path_format'])
        self.ui.LeTokutenPathFormat.setText(core.CONFIG['tokuten_path_format'])
        self.ui.LeCookie.setText(json.dumps(core.CONFIG['cookie']))
        self.ui.LeDownloadFolder.setText(core.CONFIG['download_folder'])
        self.ui.SbMaxThread.setValue(core.CONFIG['max_thread_num'])
        self.ui.CbCheckUpdateStart.setChecked(
            core.CONFIG['check_update_when_start'])
        self.ui.SbSleepTime.setValue(core.CONFIG['sleep_time'])
        self.ui.LeProxy.setText(
            core.CONFIG['proxy']['https'] if 'https' in core.CONFIG['proxy'] else "")

        # set icon
        self.ui.LIconAbout.setPixmap(core.RESOURCE["logo_pixmap"])
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])
        self.ui.PbSelect.setIcon(core.RESOURCE['open_icon'])

        # connect signals
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.PbSelect.clicked.connect(self.selectPath)
        self.ui.PbSubmit.clicked.connect(self.submitConfig)
        self.ui.PbCheckUpdate.clicked.connect(self.checkUpdate)
        self.ui.PbLogin.clicked.connect(self.showLogin)

        # thread
        self.check_update_thread = None

        # window
        self.login_window = None

    def toggleMaxState(self):
        return

    def checkUpdate(self):
        """
        Start check update thread
        """
        self.check_update_thread = CheckUpdateThread()
        self.check_update_thread.result_signal.connect(self.handleCheckUpdate)
        self.check_update_thread.start()
        self.ui.PbCheckUpdate.setDisabled(True)

    def handleCheckUpdate(self, new, detail):
        """
        Pop message box when there is a new version
        """
        if new:
            QMessageBox(QMessageBox.Information, '检测到新版本', '版本{}现已发布,\n{}\n'.format(
                detail['version'], detail['detail'])).exec()
        else:
            QMessageBox(QMessageBox.Information, '检查更新', '{}'.format(
                detail['msg'])).exec()
        self.ui.PbCheckUpdate.setDisabled(False)

    def selectPath(self):
        """
        Pop out select dialog, use absolute path
        use relative path manually
        """
        dir = QFileDialog.getExistingDirectory(
            None, "选取默认下载路径", self.ui.LeDownloadFolder.text())
        if dir == "":
            return
        self.ui.LeDownloadFolder.setText(dir)

    def submitConfig(self):
        """
        Set and update configs
        """
        config = {}
        config['cookie'] = json.loads(self.ui.LeCookie.text())
        config['download_folder'] = self.ui.LeDownloadFolder.text()
        config['max_thread_num'] = self.ui.SbMaxThread.value()
        config['check_update_when_start'] = self.ui.CbCheckUpdateStart.isChecked()
        config['sleep_time'] = self.ui.SbSleepTime.value()
        config['style'] = list(core.STYLE_CHOICE.keys())[list(
            core.STYLE_CHOICE.values()).index(self.ui.CbStyle.currentText())]
        config['proxy'] = {"https:": self.ui.LeProxy.text(
        )} if self.ui.LeProxy.text() != "" else {}
        config['path_format'] = self.ui.LePathFormat.text()
        config['tokuten_path_format'] = self.ui.LeTokutenPathFormat.text()
        core.set_config(config)
        service.update_session()
        self.close()

    def closeEvent(self, event) -> None:
        """
        Terminate all threads before window closed
        """
        if self.check_update_thread is not None and self.check_update_thread.isRunning():
            self.check_update_thread.terminate()
        if self.login_window is not None and self.login_window.isVisible():
            self.login_window.close()
        event.accept()

    def showLogin(self):
        """
        show Login window
        """
        if self.login_window is None or not self.login_window.isVisible():
            self.login_window = LoginWebWindow()
            self.login_window.cookieSignal.connect(self.updateCookie)
            self.login_window.show()

    def updateCookie(self, cookie):
        """
        Update when window closed
        """
        # if SESSDATA in cookie then success
        if 'SESSDATA' in cookie:
            self.ui.LeCookie.setText(json.dumps(cookie))


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = SettingsWindow()
    widget.show()

    sys.exit(app.exec())
