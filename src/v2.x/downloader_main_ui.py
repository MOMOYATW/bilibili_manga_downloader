import sys
import core
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
from dark_listener_thread import DarkListenerThread
import darkdetect


class MainWindow(WindowsFramelessWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set style sheet
        # check if auto set
        if core.CONFIG['style_change_with_system']:
            if darkdetect.theme() == "Dark":
                core.set_config({'style': 'dark.qss'})
            else:
                core.set_config({'style': 'light.qss'})
        self.setStyleSheet(core.QSS)

        # set ui text
        self.ui.LTitle.setText('哔哩哔哩漫画下载器')
        self.setWindowTitle('哔哩哔哩漫画下载器')
        self.ui.LeSearchBar.setPlaceholderText("输入关键词搜索或者输入网址进行解析")

        # set ui icons
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])
        self.ui.PbSettings.setIcon(core.RESOURCE["settings_icon"])
        self.PbSearch = self.ui.LeSearchBar.addAction(
            core.RESOURCE["search_icon"], QLineEdit.TrailingPosition)

        # connect signals
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.PbSettings.clicked.connect(self.showSettings)
        self.PbSearch.triggered.connect(self.startSearch)
        self.ui.LeSearchBar.textChanged.connect(
            lambda: self.ui.LeSearchBar.style().polish(self.ui.LeSearchBar))
        self.ui.LeSearchBar.returnPressed.connect(self.startSearch)

        # check update if need
        if core.CONFIG['check_update_when_start']:
            self.check_update_thread = CheckUpdateThread()
            self.check_update_thread.result_signal.connect(
                self.showCheckResult)
            self.check_update_thread.start()

        # threads
        self.loadThread = {}        # can load multiple image at same time
        self.searchThread = None    # can only search once a time
        self.darkListenerThread = None
        self.darkListenerThread = DarkListenerThread()
        self.darkListenerThread.start()
        if core.CONFIG['style_change_with_system']:
            self.darkListenerThread.themeChangedSignal.connect(
                self.themeChangedHandler)

        # windows
        self.parseWindowManager = ParseWindowManager()
        self.detailWindowManager = DetailWindowManager()
        self.settingsWindow = None

        # manage when and how to download items, the most complicated thread
        # it runs from beginning to end
        self.downloadManagerThread = DownloadManagerThread()

        # connect slots
        self.parseWindowManager.addTaskSignal = self.downloadManagerThread.createDownloadTasks
        self.parseWindowManager.requestTaskInListSignal = self.downloadManagerThread.sendTaskToParse
        self.detailWindowManager.createParseSignal = self.parseWindowManager.createWindow
        self.detailWindowManager.requestTaskInListSignal = self.downloadManagerThread.sendTaskToDetail
        self.downloadManagerThread.feedback_task_signal.connect(
            self.addDownloadTask
        )
        self.downloadManagerThread.update_task_status_signal.connect(
            self.updateRowInTableDownloadStatus
        )
        self.downloadManagerThread.update_task_progress_signal.connect(
            self.updateRowInTableDownloadProgress
        )
        self.downloadManagerThread.response_parse_signal.connect(
            self.parseWindowManager.passToParseWindow
        )
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

    def startSearch(self):
        """ Get content in search bar and start search thread """
        # disable action
        self.__toggleSearchBar()
        # get content in lineedit
        search_content = self.ui.LeSearchBar.text()
        # start thread
        self.searchThread = SearchThread(search_content)
        self.searchThread.msgSignal.connect(lambda msg: print(msg))
        self.searchThread.addTaskSignal.connect(
            self.downloadManagerThread.createDownloadTasks)
        # self.searchThread.single_result_signal.connect(
        #     self.addDownloadTask)
        self.searchThread.createParseSignal.connect(
            self.parseWindowManager.createWindow)
        self.searchThread.finished.connect(self.__toggleSearchBar)
        self.searchThread.start()

    def themeChangedHandler(self, theme):
        if theme == "Dark":
            core.set_config({'style': 'dark.qss'})
        else:
            core.set_config({'style': 'light.qss'})
        self.updateSettings()

    def __toggleSearchBar(self):
        """ Enable or disable the search bar """
        if self.ui.LeSearchBar.isEnabled():
            self.ui.LeSearchBar.setDisabled(True)
            self.PbSearch.triggered.disconnect()
            self.ui.LeSearchBar.returnPressed.disconnect()
        else:
            self.ui.LeSearchBar.returnPressed.connect(self.startSearch)
            self.PbSearch.triggered.connect(self.startSearch)
            self.ui.LeSearchBar.setDisabled(False)
            self.ui.LeSearchBar.setFocus()

    def showCheckResult(self, new, detail):
        """ If a new version is detected, pop out a msg box """
        # TODO: 可以考虑换一种形式提示结果，如在某处显示 有新版本 等
        if new:
            QMessageBox(QMessageBox.Information, '检测到新版本', '版本{}现已发布,\n{}\n'.format(
                detail['version'], detail['detail'])).exec()

    def showSettings(self):
        """ Open settings window """
        if self.settingsWindow is None or not self.settingsWindow.isVisible():
            self.settingsWindow = SettingsWindow()
            self.settingsWindow.updateSettingsSignal.connect(
                self.updateSettings)
        self.settingsWindow.show()

    def updateSettings(self):
        self.setStyleSheet(core.QSS)
        self.parseWindowManager.updateSettings()
        self.detailWindowManager.updateSettings()
        self.downloadManagerThread.dispatch()
        if self.settingsWindow is not None:
            self.settingsWindow.updateSettings()
        if not core.CONFIG['style_change_with_system']:
            self.darkListenerThread.themeChangedSignal.connect(None)
        else:
            self.darkListenerThread.themeChangedSignal.connect(
                self.themeChangedHandler)

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["restore_icon"])

    def addDownloadTask(self, new_manga, manga_task):
        """ Update UI """
        if new_manga:
            self.insertRowInTable(manga_task)
            return
        self.updateRowInTableTaskNum(manga_task)

    def insertRowInTable(self, manga_task):
        """ Insert a row """
        manga_id = manga_task['info']['id']
        cover_url = manga_task['info']['horizontal_cover']

        self.loadThread[manga_id] = FetchThread(cover_url)
        self.loadThread[manga_id].resoponse_signal.connect(
            lambda content: self.updateRowInTableCover(content, manga_id))
        self.loadThread[manga_id].start()

        download_task_item = DownloadTaskItem(manga_task)
        download_task_item.double_click_signal.connect(
            self.detailWindowManager.createWindow)

        item = QListWidgetItem()
        item.setSizeHint(download_task_item.sizeHint())
        self.ui.LwTaskList.addItem(item)
        self.ui.LwTaskList.setItemWidget(item, download_task_item)

    def updateRowInTableTaskNum(self, manga_task):
        """ Update the row task num """
        # TODO: for循环效率太低，可以用字典
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_task['info']['id']:
                widget.updateTaskNum(manga_task)
                break

    def updateRowInTableDownloadStatus(self, manga_id, status):
        """ Update the row task status """
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateTaskStatus(status)
                break

    def updateRowInTableDownloadProgress(self, manga_id, value):
        """ Update the row task progress """
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateProgress(value * 100)
                break

    def updateRowInTableCover(self, content, manga_id):
        """ Update the row task cover """
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
        """ Overload function """
        # terminate all thread
        # TODO: 如果下载尚未结束最好提示用户，并且最好不要用terminate结束
        for key in self.loadThread:
            self.loadThread[key].terminate()
        if self.searchThread is not None and self.searchThread.isRunning():
            self.searchThread.terminate()
        self.downloadManagerThread.terminate()
        self.darkListenerThread.terminate()

        # close all window
        if self.settingsWindow is not None:
            self.settingsWindow.close()
        self.parseWindowManager.closeAll()
        self.detailWindowManager.closeAll()

        core.save_config_file()
        sys.exit(0)


if __name__ == '__main__':
    """
    create and show window
    """
    pass
