import sys
import os
import sources_rc
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QLineEdit, QListWidgetItem, QMessageBox
from fetch_thread import FetchThread
from search_thread import SearchThread
from frameless_window import WindowsFramelessWindow
from downloader_main_base_ui import Ui_MainWindow
from downloader_settings_ui import SettingsWindow
from downloader_task_item_ui import DownloadTaskItem
from downloader_task_detail_ui import TaskDetailWindow
from core import read_config_file, save_config_file, VERSION_TAG
from check_update_thread import CheckUpdateThread
from parse_window_manager import ParseWindowManager
from download_manager_thread import DownloadManagerThread


class MainWindow(WindowsFramelessWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadResources()

        self.ui.LTitle.setText('哔哩哔哩漫画下载器 {}'.format(VERSION_TAG))
        self.setWindowTitle('哔哩哔哩漫画下载器 {}'.format(VERSION_TAG))
        self.setWindowIcon(self.resource["logo_icon"])
        self.ui.LIcon.setPixmap(self.resource["logo_pixmap"])
        self.ui.PbMinimize.setIcon(self.resource["minimize_icon"])
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])
        self.ui.PbClose.setIcon(self.resource["close_icon"])
        self.search_btn = self.ui.LeSearchBar.addAction(
            self.resource["search_icon"], QLineEdit.TrailingPosition)
        self.search_btn.triggered.connect(self.startSearch)
        self.ui.PbSettings.setIcon(self.resource["settings_icon"])
        self.ui.LeSearchBar.setPlaceholderText("输入关键词搜索或者输入网址进行解析")
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.LeSearchBar.textChanged.connect(
            lambda: self.ui.LeSearchBar.style().polish(self.ui.LeSearchBar))
        self.ui.LeSearchBar.returnPressed.connect(self.startSearch)
        self.ui.PbSettings.clicked.connect(self.showSettings)

        self.config = read_config_file({"cookie": {},
                                        "width": 1100,
                                        "download_folder": "./",
                                        "max_thread_num": 1,
                                        "check_update_when_start": True,
                                        "sleep_time": 1000})

        if self.config['check_update_when_start']:
            self.check_update_thread = CheckUpdateThread()
            self.check_update_thread.result_signal.connect(
                self.showCheckResult)
            self.check_update_thread.start()

        self.loadThread = {}
        self.searchThread = None
        self.taskDetail = None

        self.parseWindowManager = ParseWindowManager(self.resource, self.qss)
        self.settingsWindow = None
        self.downloadManagerThread = DownloadManagerThread(self.config)
        self.downloadManagerThread.send_task_signal.connect(
            self.downloadManagerThread.createDownloadTasks)
        self.downloadManagerThread.feedback_task_signal.connect(
            self.addDownloadTask)
        self.downloadManagerThread.update_task_singal.connect(
            self.updateRowInTableDownloadStatus
        )
        self.downloadManagerThread.start()

    def loadResources(self):
        """ Load all resources """
        # fetch style sheet path
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = "./"
        styleFile = os.path.join(base_path, 'style.qss')
        # set style sheet
        with open(styleFile, 'r') as f:
            self.qss = f.read()
            self.setStyleSheet(self.qss)

        # load from sources_rc
        self.resource = {}
        self.resource["logo_pixmap"] = QPixmap(
            QPixmap(u":/imgs/icon.png"))
        self.resource["logo_icon"] = QIcon()
        self.resource["logo_icon"].addFile(
            u":/imgs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["close_icon"] = QIcon()
        self.resource["close_icon"].addFile(
            u":/imgs/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["minimize_icon"] = QIcon()
        self.resource["minimize_icon"].addFile(
            u":/imgs/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["maximize_icon"] = QIcon()
        self.resource["maximize_icon"].addFile(
            u":/imgs/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["restore_icon"] = QIcon()
        self.resource["restore_icon"].addFile(
            u":/imgs/windowed.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["search_icon"] = QIcon()
        self.resource["search_icon"].addFile(
            u":/imgs/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["settings_icon"] = QIcon()
        self.resource["settings_icon"].addFile(
            u":/imgs/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["play_icon"] = QIcon()
        self.resource["play_icon"].addFile(
            u":/imgs/start.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["pause_icon"] = QIcon()
        self.resource["pause_icon"].addFile(
            u":/imgs/pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resource["open_icon"] = QIcon()
        self.resource["open_icon"].addFile(
            u":/imgs/open.png", QSize(), QIcon.Normal, QIcon.Off)

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
        self.searchThread = SearchThread(search_content, self.config)
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
        parseWindow.show()

    def showSettings(self):
        """ Open settings window """
        if self.settingsWindow is None or not self.settingsWindow.isVisible():
            self.settingsWindow = SettingsWindow(
                self.resource, self.qss, self.config)
            self.settingsWindow.update_settings_signal.connect(
                self.updateConfig)
        self.settingsWindow.show()

    def updateConfig(self, config):
        self.config = config

    def showTaskDetail(self, manga_id):
        """ Open task detail window"""
        pass

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["restore_icon"])

    def deleteTask(self):
        pass

    def addDownloadTask(self, new_manga, manga_task):
        if new_manga:
            self.insertRowInTable(manga_task)
            return
        self.updateRowInTable(manga_task)

    def insertRowInTable(self, manga_task):
        manga_id = manga_task['info']['id']
        cover_url = manga_task['info']['horizontal_cover']
        self.loadThread[manga_id] = FetchThread(cover_url, None)
        self.loadThread[manga_id].resoponse_signal.connect(
            lambda content: self.loadImage(content, manga_id))
        self.loadThread[manga_id].start()

        download_task_item = DownloadTaskItem(manga_task)
        # download_task_item.double_click_signal.connect(self.showTaskDetail)
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

    def updateRowInTableDownloadStatus(self, manga_id, status, value):
        for i in range(self.ui.LwTaskList.count()):
            item = self.ui.LwTaskList.item(i)
            widget = self.ui.LwTaskList.itemWidget(item)
            if widget.manga_id == manga_id:
                widget.updateTaskStatus(status)
                widget.updateProgress(value)

    def loadImage(self, content, manga_id):
        cover = QPixmap()
        cover.loadFromData(content)
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
        save_config_file(self.config)
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
