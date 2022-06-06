import sys
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QApplication, QListWidgetItem, QAbstractItemView
from fetch_thread import FetchThread
from frameless_window import WindowsFramelessWindow
from downloader_parse_base_ui import Ui_MainWindow
import core


class ParseResultWindow(WindowsFramelessWindow):
    addTaskSignal = Signal(dict)
    closedSignal = Signal(int)

    def __init__(self, parse_result) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set style sheet
        self.setStyleSheet(core.QSS)

        #
        self.ep_list = parse_result['ep_list']
        self.tokuten = parse_result['tokuten']
        self.manga_info = parse_result
        parse_result['ep_list'].reverse()
        parse_result['tokuten'].reverse()
        parse_result.pop('ep_list')
        parse_result.pop('tokuten')

        self.setWindowTitle('漫画详情')
        self.ui.LTitle.setText('解析结果')
        self.setWindowIcon(core.RESOURCE["logo_icon"])
        self.ui.LIcon.setPixmap(core.RESOURCE["logo_pixmap"])
        self.ui.PbMinimize.setIcon(core.RESOURCE["minimize_icon"])
        self.ui.PbClose.setIcon(core.RESOURCE["close_icon"])
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)

        self.ui.LMangaTitle.setText(self.manga_info['title'])
        self.ui.LAuthor.setText(", ".join(str(i)
                                for i in self.manga_info['author_name']))
        self.ui.LDescription.setText(self.manga_info['classic_lines'] + '\n')

        self.fetch_thread = FetchThread(self.manga_info['vertical_cover'])
        self.fetch_thread.resoponse_signal.connect(self.loadImage)
        self.fetch_thread.start()
        self.ui.PbDownload.setText('开始下载')
        self.ui.LChapterTitle.setText('章节列表')
        self.ui.PbCancelAll.setText('取消全部')
        self.ui.PbSelectAll.setText('选择全部')

        self.ui.PbSelectAll.clicked.connect(self.selectAll)
        self.ui.PbCancelAll.clicked.connect(self.cancelAll)
        self.ui.PbDownload.clicked.connect(self.addToDownloadList)

        self.ui.LwChapterList.setSelectionMode(
            QAbstractItemView.MultiSelection)

        for i in range(len(self.ep_list)):
            item = QListWidgetItem()
            item.setText('{}  {}'.format(
                self.ep_list[i]['short_title'], self.ep_list[i]['title']))

            if self.ep_list[i]['is_locked']:
                item.setFlags(item.flags() & Qt.NoItemFlags)
                item.setText("{} - 漫币：{}".format(item.text(),
                             self.ep_list[i]['pay_gold']))
            item.setSizeHint(QSize(0, 50))
            self.ui.LwChapterList.addItem(item)

        for i in range(len(self.tokuten)):
            item = QListWidgetItem()
            item.setText('{}  {}'.format(
                self.tokuten[i]['item']['title'], self.tokuten[i]['item']['detail']))

            if self.tokuten[i]['isLock']:
                item.setFlags(item.flags() & Qt.NoItemFlags)
            item.setSizeHint(QSize(0, 50))
            self.ui.LwChapterList.addItem(item)

    def loadImage(self, content):
        Cover = QPixmap()
        Cover.loadFromData(content)
        self.ui.LCover.setPixmap(Cover)

    def selectAll(self):
        """ select all items """
        for i in range(self.ui.LwChapterList.count()):
            item = self.ui.LwChapterList.item(i)
            if item.flags != Qt.NoItemFlags:
                item.setSelected(True)
            else:
                item.setSelected(False)

    def cancelAll(self):
        """ cancel all items """
        for i in range(self.ui.LwChapterList.count()):
            item = self.ui.LwChapterList.item(i)
            item.setSelected(False)

    def addToDownloadList(self):
        downloaditems = self.manga_info
        downloaditems['list'] = []
        downloaditems['tokuten'] = []
        for i in range(len(self.ep_list)):
            item = self.ui.LwChapterList.item(i)
            if item.isSelected():
                downloaditems['list'].append(self.ep_list[i])
        for i in range(len(self.tokuten)):
            item = self.ui.LwChapterList.item(len(self.ep_list) + i)
            if item.isSelected():
                downloaditems['tokuten'].append(self.tokuten[i])
        if len(downloaditems['list']) == 0 and len(downloaditems['tokuten']) == 0:
            print('no items')
            return
        self.addTaskSignal.emit(downloaditems)
        self.close()

    def applyTaskInList(self, tasks):
        if tasks == {}:
            return
        for i in range(len(self.ep_list)):
            item = self.ui.LwChapterList.item(i)
            if self.ep_list[i]['id'] in tasks:
                item.setSelected(True)
                item.setFlags(item.flags() & Qt.NoItemFlags)
                item.setText(
                    '{} {} - {}'.format(self.ep_list[i]['short_title'], self.ep_list[i]['title'], '已添加到任务列表中'))

        for i in range(len(self.tokuten)):
            item = self.ui.LwChapterList.item(len(self.ep_list) + i)
            if self.tokuten[i]['item']['id'] in tasks:
                item.setSelected(True)
                item.setFlags(item.flags() & Qt.NoItemFlags)
                item.setText(
                    '{} {} - {}'.format(self.tokuten[i]['item']['title'], self.tokuten[i]['item']['detail'], '已添加到任务列表中'))

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(core.RESOURCE["restore_icon"])

    def closeEvent(self, event) -> None:
        # check if thread is running
        if self.fetch_thread.isRunning():
            self.fetch_thread.terminate()
        self.closedSignal.emit(self.manga_info['id'])
        event.accept()


if __name__ == '__main__':
    """
    create and show window
    """
    pass
