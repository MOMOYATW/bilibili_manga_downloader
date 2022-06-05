import sys
from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import QApplication, QListWidgetItem
from frameless_window import WindowsFramelessWindow
from downloader_task_detail_base_ui import Ui_MainWindow
from downloader_task_item_ui import DownloadTaskItem
from search_thread import SearchThread


class TaskDetailWindow(WindowsFramelessWindow):
    closedSignal = Signal(int)
    searchSignal = Signal(dict)

    def __init__(self, manga_id, resource={}, qss="", config={}) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resource = resource
        self.setStyleSheet(qss)
        self.config = config
        self.manga_id = manga_id
        self.list = {}
        self.setWindowTitle('任务详情')
        self.ui.LTitle.setText('任务详情')
        self.setWindowIcon(self.resource["logo_icon"])
        self.ui.LIcon.setPixmap(self.resource["logo_pixmap"])
        self.ui.PbMinimize.setIcon(self.resource["minimize_icon"])
        self.ui.PbClose.setIcon(self.resource["close_icon"])
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)
        self.ui.PbParsePage.clicked.connect(self.startSearch)

        self.ui.LChapterTitle.setText('下载列表')
        self.ui.PbStartResumeAll.setText('')
        self.ui.PbParsePage.setText('前往漫画')

    def startSearch(self):
        self.searchThread = SearchThread(
            'manga.bilibili.com/detail/mc{}'.format(self.manga_id), {'cookie': self.config['cookie']})
        self.searchThread.message_signal.connect(lambda msg: print(msg))
        self.searchThread.finished.connect(
            lambda: self.ui.PbParsePage.setDisabled(False))
        self.searchThread.episodes_result_signal.connect(
            self.searchSignal.emit)
        self.searchThread.start()

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["restore_icon"])

    def closeEvent(self, event) -> None:
        self.closedSignal.emit(self.manga_id)

        event.accept()

    def applyTaskInList(self, tasks):
        if tasks == {}:
            return
        self.list.update(tasks)
        self.ui.LwChapterList.clear()
        for i in self.list:
            if i == 'info':
                continue
            download_task_item = DownloadTaskItem(self.list[i], total=False)
            download_task_item.updateTaskCover(
                self.resource['cover'][self.manga_id])
            item = QListWidgetItem()
            item.setSizeHint(download_task_item.sizeHint())
            self.ui.LwChapterList.addItem(item)
            self.ui.LwChapterList.setItemWidget(item, download_task_item)

    def updateProgress(self, index, value):
        item = self.ui.LwChapterList.item(list(self.list).index(index) - 1)
        widget = self.ui.LwChapterList.itemWidget(item)
        widget.updateProgress(value * 100)

    def updateTaskStatus(self, index, status):
        item = self.ui.LwChapterList.item(list(self.list).index(index) - 1)
        widget = self.ui.LwChapterList.itemWidget(item)
        widget.updateTaskStatus(status)


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = TaskDetailWindow()
    widget.show()

    sys.exit(app.exec())
