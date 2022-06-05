import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget
from downloader_task_item_base_ui import Ui_Form


class DownloadTaskItem(QWidget):
    double_click_signal = Signal(int)

    def __init__(self, task_info, resource={}, qss="", total=True) -> None:
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.resource = resource
        self.setStyleSheet(qss)
        self.total = total
        if total:
            self.manga_id = task_info['info']['id']
            self.ui.LItemTitle.setText(task_info['info']['title'])
            self.ui.LItemStatus.setText('排队中')
            self.ui.LItemCount.setText(
                '共{}个任务'.format(len(task_info) - 1))
            self.ui.PbProgress.setValue(0)
        else:
            if task_info['type'] == 'honpen':
                self.ui.LItemTitle.setText("{} {}".format(
                    task_info['short_title'], task_info['title']))
            else:
                self.ui.LItemTitle.setText("{} {}".format(
                    task_info['item']['title'], task_info['item']['detail']
                ))
            if task_info['status'] == 'pending':
                self.ui.LItemStatus.setText('排队中')
            elif task_info['status'] == 'running':
                self.ui.LItemStatus.setText('下载中')
            elif task_info['status'] == 'finished':
                self.ui.LItemStatus.setText('已完成')
            else:
                self.ui.LItemStatus.setText('部分失败')
            self.ui.LItemCount.setText('')
            self.ui.PbProgress.setValue(task_info['progress'] * 100)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and self.total:
            self.double_click_signal.emit(self.manga_id)

    def enterEvent(self, event) -> None:
        self.ui.FItem.setProperty('status', 'hover')
        self.ui.FItem.style().polish(self.ui.FItem)

    def leaveEvent(self, event) -> None:
        if self.ui.FItem.property('status') == 'hover':
            self.ui.FItem.setProperty('status', 'unfocus')
            self.ui.FItem.style().polish(self.ui.FItem)

    def updateTaskNum(self, task_info):
        self.ui.LItemCount.setText(
            '共{}个任务'.format(len(task_info) - 1))

    def updateTaskCover(self, content):
        self.ui.LItemCover.setPixmap(content)

    def updateTaskStatus(self, status):
        self.ui.LItemStatus.setText(status)

    def updateProgress(self, value):
        self.ui.PbProgress.setValue(value)
        self.update()


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)
    styleFile = './style.qss'
    # set style sheet
    with open(styleFile, 'r') as f:
        qss = f.read()
    widget = DownloadTaskItem(qss=qss)
    widget.show()

    sys.exit(app.exec())
