import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from frameless_window import WindowsFramelessWindow
from downloader_task_detail_base_ui import Ui_MainWindow
from fetch_thread import FetchThread


class TaskDetailWindow(WindowsFramelessWindow):
    def __init__(self, detail, resource={}, qss="") -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resource = resource
        self.setStyleSheet(qss)
        self.detail = detail

        self.ui.LTitle.setText('任务详情')
        self.setWindowIcon(self.resource["logo_icon"])
        self.ui.LIcon.setPixmap(self.resource["logo_pixmap"])
        self.ui.PbMinimize.setIcon(self.resource["minimize_icon"])
        self.ui.PbClose.setIcon(self.resource["close_icon"])
        self.ui.PbMinimize.clicked.connect(self.window().showMinimized)
        self.ui.PbClose.clicked.connect(self.close)
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])
        self.ui.PbMaximizeRestore.clicked.connect(self.toggleMaxState)

        self.ui.LMangaTitle.setText(self.detail['info']['title'])
        self.ui.LAuthor.setText(", ".join(str(i)
                                for i in self.detail['info']['author_name']))
        self.ui.LDescription.setText('')
        self.fetch_thread = FetchThread(
            self.detail['info']['horizontal_cover'], None)
        self.fetch_thread.resoponse_signal.connect(self.loadImage)
        self.fetch_thread.start()

    def changeIconMaximized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["maximize_icon"])

    def changeIconNormalized(self):
        """ overload function """
        self.ui.PbMaximizeRestore.setIcon(self.resource["restore_icon"])

    def loadImage(self, content):
        Cover = QPixmap()
        Cover.loadFromData(content)
        self.ui.LCover.setPixmap(Cover)


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = TaskDetailWindow()
    widget.show()

    sys.exit(app.exec())
