import os
import sys
import core
import sources_rc
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLineEdit, QListWidgetItem, QMessageBox
from fetch_thread import FetchThread
from search_thread import SearchThread
from check_update_thread import CheckUpdateThread
from download_manager_thread import DownloadManagerThread
from parse_window_manager import ParseWindowManager
from detail_window_manager import DetailWindowManager
from frameless_window import WindowsFramelessWindow
from downloader_main_base_ui import Ui_MainWindow
from downloader_settings_ui import SettingsWindow
from downloader_task_item_ui import DownloadTaskItem


class MainWindow(WindowsFramelessWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(core.QSS)

        self.ui.LTitle.setText('哔哩哔哩漫画下载器 {}'.format(core.VERSION_TAG))
        self.setWindowTitle('哔哩哔哩漫画下载器 {}'.format(core.VERSION_TAG))
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])
        self.search_btn = self.ui.LeSearchBar.addAction(
            core.RESOURCE["search_icon"], QLineEdit.TrailingPosition)
        self.search_btn.triggered.connect(self.startSearch)
        self.ui.PbSettings.setIcon(core.RESOURCE["settings_icon"])
        self.ui.LeSearchBar.setPlaceholderText("输入关键词搜索或者输入网址进行解析")
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.LeSearchBar.textChanged.connect(
            lambda: self.ui.LeSearchBar.style().polish(self.ui.LeSearchBar))
        self.ui.LeSearchBar.returnPressed.connect(self.startSearch)
        self.ui.PbSettings.clicked.connect(self.showSettings)

        if core.CONFIG['check_update_when_start']:
            self.check_update_thread = CheckUpdateThread()
            self.check_update_thread.result_signal.connect(
                self.showCheckResult)
            self.check_update_thread.start()

        self.loadThread = {}
        self.searchThread = None
        self.taskDetail = None

        self.parseWindowManager = ParseWindowManager()
        self.detailWindowManager = DetailWindowManager(self.showResultWindow)
        self.settingsWindow = None
        self.downloadManagerThread = DownloadManagerThread()
        self.downloadManagerThread.send_task_signal.connect(
            self.downloadManagerThread.createDownloadTasks)
        self.downloadManagerThread.feedback_task_signal.connect(
            self.addDownloadTask)
        self.downloadManagerThread.update_task_status_signal.connect(
            self.updateRowInTableDownloadStatus
        )
        self.downloadManagerThread.update_task_progress_signal.connect(
            self.updateRowInTableDownloadProgress
        )
        self.downloadManagerThread.response_parse_signal.connect(
            self.parseWindowManager.passToParseWindow)
        self.downloadManagerThread.response_detail_signal.connect(
            self.detailWindowManager.passToDetailWindow
        )
        self.downloadManagerThread.update_detail_progress_signal.connect(
            self.detailWindowManager.updateDetailProgress
        )
        self.downloadManagerThread.update_detail_status_signal.connect(
            self.detailWindowManager.updateDetailStatus
        )
        self.downloadManagerThread.start()

    def showCheckResult(self, new, detail):
        if new:
            QMessageBox(QMessageBox.Information, '检测到新版本', '版本{}现已发布,\n{}\n'.format(
                detail['version'], detail['detail'])).exec()

    def startSearch(self):
        """ Get content in search bar and start search thread """
        # disable action
        self.__toggleSearchBar()
        # get content in lineedit
        search_content = self.ui.LeSearchBar.text()
        # start thread
        self.searchThread = SearchThread(search_content)
        self.searchThread.message_signal.connect(lambda msg: print(msg))
        # self.searchThread.single_result_signal.connect(
        #     self.addDownloadTask)
        self.searchThread.finished.connect(self.__toggleSearchBar)
        self.searchThread.episodes_result_signal.connect(
            self.showResultWindow)
        self.searchThread.start()

    def __toggleSearchBar(self):
        """ Enable or disable the search bar """
        if self.ui.LeSearchBar.isEnabled():
            self.ui.LeSearchBar.setDisabled(True)
            self.search_btn.triggered.disconnect()
            self.ui.LeSearchBar.returnPressed.disconnect()
        else:
            self.ui.LeSearchBar.returnPressed.connect(self.startSearch)
            self.search_btn.triggered.connect(self.startSearch)
            self.ui.LeSearchBar.setDisabled(False)
            self.ui.LeSearchBar.setFocus()

    def showResultWindow(self, parse_result):
        """ Open result window """
        # add window to manager
        parseWindow = self.parseWindowManager.createWindow(parse_result)
        parseWindow.addTaskSignal.connect(
            self.downloadManagerThread.send_task_signal.emit)
        self.downloadManagerThread.sendTaskToParse(parse_result['id'])
        parseWindow.show()

    def showSettings(self):
        """ Open settings window """
        if self.settingsWindow is None or not self.settingsWindow.isVisible():
            self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["restore_icon"])

    def deleteTask(self):
        pass

    def addDownloadTask(self, new_manga, manga_task):
        if new_manga:
            self.insertRowInTable(manga_task)
            return
        self.updateRowInTable(manga_task)

    def showDetailWindow(self, manga_id):
        DetailWindow = self.detailWindowManager.createWindow(manga_id)
        self.downloadManagerThread.sendTaskToDetail(manga_id)
        DetailWindow.show()

    def insertRowInTable(self, manga_task):
        manga_id = manga_task['info']['id']
        cover_url = manga_task['info']['horizontal_cover']
        self.loadThread[manga_id] = FetchThread(cover_url)
        self.loadThread[manga_id].resoponse_signal.connect(
            lambda content: self.loadImage(content, manga_id))
        self.loadThread[manga_id].start()

        download_task_item = DownloadTaskItem(manga_task)
        download_task_item.double_click_signal.connect(
            self.showDetailWindow)
        item = QListWidgetItem()
        item.setSizeHint(download_task_item.sizeHint())
        self.ui.LwTaskList.addItem(item)
        self.ui.LwTaskList.setItemWidget(item, download_task_item)

    def updateRowInTable(self, manga_task):
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_task['info']['id']:
                widget.updateTaskNum(manga_task)

    def updateRowInTableDownloadStatus(self, manga_id, status):
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateTaskStatus(status)
                break

    def updateRowInTableDownloadProgress(self, manga_id, value):
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateProgress(value * 100)
                break

    def loadImage(self, content, manga_id):
        cover = QPixmap()
        cover.loadFromData(content)
        core.RESOURCE['cover'][manga_id] = cover
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateTaskCover(cover)
        self.loadThread.pop(manga_id)

    def closeEvent(self, event) -> None:
        # terminate all thread
        for key in self.loadThread:
            self.loadThread[key].terminate()
        if self.searchThread is not None and self.searchThread.isRunning():
            self.searchThread.terminate()
        self.downloadManagerThread.terminate()
        # close all window
        if self.settingsWindow is not None:
            self.settingsWindow.close()
        self.parseWindowManager.closeAll()
        sys.exit(0)


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    print(os.name)
    sys.exit(app.exec())
