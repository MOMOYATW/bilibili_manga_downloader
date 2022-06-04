import sys
import os
import json
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from frameless_window import WindowsFramelessWindow
from downloader_settings_base_ui import Ui_MainWindow
from check_update_thread import CheckUpdateThread


class SettingsWindow(WindowsFramelessWindow):
    update_settings_signal = Signal(dict)

    def __init__(self, resource={}, qss="", config={}) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resource = resource
        self.setStyleSheet(qss)
        self.config = config

        self.ui.LTitle.setText('设置')
        self.setWindowTitle('设置')
        self.setWindowIcon(self.resource["logo_icon"])
        self.ui.LIcon.setPixmap(self.resource["logo_pixmap"])
        self.ui.PbMinimize.setIcon(self.resource["minimize_icon"])
        self.ui.PbClose.setIcon(self.resource["close_icon"])
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.LCookie.setText('登录账户Cookie')
        self.ui.LImageWidth.setText('下载图片宽度')
        self.ui.LDownloadFolder.setText('下载根目录')
        self.ui.LMaxThread.setText('最大下载线程数')
        self.ui.LCheckUpdateStart.setText('启动时检查更新')
        self.ui.LSleepTime.setText('下载间隔时间')
        self.ui.PbSubmit.setText('保存设置')
        self.ui.LeCookie.setText(json.dumps(self.config['cookie']))
        if self.config['width'] is None:
            self.ui.SbImageWidth.setDisabled(True)
            self.ui.SbImageWidth.setMaximum(9999)
            self.ui.SbImageWidth.setValue(9999)
        else:
            self.ui.SbImageWidth.setValue(self.config['width'])
        self.ui.LeDownloadFolder.setText(self.config['download_folder'])
        self.ui.SbMaxThread.setValue(self.config['max_thread_num'])
        self.ui.CbCheckUpdateStart.setChecked(
            self.config['check_update_when_start'])
        self.ui.SbSleepTime.setValue(self.config['sleep_time'])
        self.ui.PbSelect.setIcon(self.resource['open_icon'])
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
            QMessageBox(QMessageBox.Information, '恭喜', '当前版本是最新版{}'.format(
                detail['version'])).exec()
        self.ui.PbCheckUpdate.setDisabled(False)

    def selectPath(self):
        """
        Pop out select dialog, if user select a sub path, then use relative path
        else use absolute path
        """
        dir = QFileDialog.getExistingDirectory(
            None, "选取默认下载路径", self.ui.LeDownloadFolder.text())
        if dir == "":
            return
        rel_path = os.path.relpath(dir)
        if rel_path.find('..') == -1:
            dir = os.path.join('.', rel_path)
        self.ui.LeDownloadFolder.setText(dir)

    def submitConfig(self):
        self.config['cookie'] = json.loads(self.ui.LeCookie.text())
        self.config['width'] = self.ui.SbImageWidth.value()
        self.config['download_folder'] = self.ui.LeDownloadFolder.text()
        self.config['max_thread_num'] = self.ui.SbMaxThread.value()
        self.config['check_update_when_start'] = self.ui.CbCheckUpdateStart.isChecked()
        self.config['sleep_time'] = self.ui.SbSleepTime.value()
        self.update_settings_signal.emit(self.config)
        self.close()

    def closeEvent(self, event) -> None:
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
