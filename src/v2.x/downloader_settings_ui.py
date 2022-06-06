import sys
import os
import json
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from frameless_window import WindowsFramelessWindow
from downloader_settings_base_ui import Ui_MainWindow
from check_update_thread import CheckUpdateThread
import core
import service


class SettingsWindow(WindowsFramelessWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet(core.QSS)

        self.ui.LTitle.setText('设置')
        self.setWindowTitle('设置')
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.LCookie.setText('登录账户Cookie')
        self.ui.LDownloadFolder.setText('下载根目录')
        self.ui.LMaxThread.setText('最大下载线程数')
        self.ui.LCheckUpdateStart.setText('启动时检查更新')
        self.ui.LSleepTime.setText('下载间隔时间')
        self.ui.PbSubmit.setText('保存设置')
        self.ui.LeCookie.setText(json.dumps(core.CONFIG['cookie']))
        self.ui.LeDownloadFolder.setText(core.CONFIG['download_folder'])
        self.ui.SbMaxThread.setValue(core.CONFIG['max_thread_num'])
        self.ui.CbCheckUpdateStart.setChecked(
            core.CONFIG['check_update_when_start'])
        self.ui.SbSleepTime.setValue(core.CONFIG['sleep_time'])
        self.ui.PbSelect.setIcon(core.RESOURCE['open_icon'])
        self.ui.PbSelect.clicked.connect(self.selectPath)
        self.ui.PbSubmit.clicked.connect(self.submitConfig)
        self.ui.PbCheckUpdate.setText('检查更新')
        self.ui.PbCheckUpdate.clicked.connect(self.checkUpdate)
        self.check_update_thread = None

    def toggleMaxState(self):
        return

    def checkUpdate(self):
        self.check_update_thread = CheckUpdateThread()
        self.check_update_thread.result_signal.connect(self.handleCheckUpdate)
        self.check_update_thread.start()
        self.ui.PbCheckUpdate.setDisabled(True)

    def handleCheckUpdate(self, new, detail):
        if new:
            QMessageBox(QMessageBox.Information, '检测到新版本', '版本{}现已发布,\n{}\n'.format(
                detail['version'], detail['detail'])).exec()
        else:
            QMessageBox(QMessageBox.Information, '检查更新', '{}'.format(
                detail)).exec()
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
        core.CONFIG['cookie'] = json.loads(self.ui.LeCookie.text())
        core.CONFIG['download_folder'] = self.ui.LeDownloadFolder.text()
        core.CONFIG['max_thread_num'] = self.ui.SbMaxThread.value()
        core.CONFIG['check_update_when_start'] = self.ui.CbCheckUpdateStart.isChecked()
        core.CONFIG['sleep_time'] = self.ui.SbSleepTime.value()
        service.update_cookie()
        self.close()

    def closeEvent(self, event) -> None:
        """
        Terminate all threads before window closed
        """
        if self.check_update_thread is not None and self.check_update_thread.isRunning():
            self.check_update_thread.terminate()
        event.accept()


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = SettingsWindow()
    widget.show()

    sys.exit(app.exec())
