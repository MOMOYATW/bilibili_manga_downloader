import sys
from PySide6.QtCore import Qt
from CustomWindow import CustomWindow
from terminal_downloader import *
from settings_base_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QGraphicsDropShadowEffect


class SettingWindow(CustomWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.maximize = False
        self.edge_scaling = False
        self.title_bar_height = self.ui.title_bar.height()
        self.outermost_layout = self.ui.outermost_layout
        self.main_widget = self.ui.background

        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_min.clicked.connect(self.showMinimized)
        self.ui.btn_select.clicked.connect(self.selectPath)

        self.drawShadow()
        self.loadStyleSheet()

    def selectPath(self):
        """
        Pop out select dialog, if user select a sub path, then use relative path
        else use absolute path
        """
        dir = QFileDialog.getExistingDirectory(
            None, "选取默认下载路径", self.ui.path_input.text())
        if dir == "":
            return
        rel_path = os.path.relpath(dir)
        if rel_path.find('..') == -1:
            dir = os.path.join('.', rel_path)
        self.ui.path_input.setText(dir)

    def loadStyleSheet(self):
        """
        Load qss
        """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        styleFile = 'style.qss'
        if os.path.exists(os.path.join('.', styleFile)):
            styleFile = os.path.join('.', styleFile)
        else:
            styleFile = os.path.join(base_path, 'style', styleFile)

        with open(styleFile, 'r') as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def init(self, config: dict, fetchSettings) -> None:
        self.ui.cookie_input.setText(config['cookie_text'])
        self.ui.path_input.setText(config['base_folder'])
        self.ui.spinBox.setValue(config['interval_seconds'])
        self.ui.btn_save.clicked.connect(fetchSettings)

    def getSettings(self):
        config = {}
        config['cookie_text'] = self.ui.cookie_input.text()
        config['base_folder'] = self.ui.path_input.text()
        config['interval_seconds'] = self.ui.spinBox.value()
        return config


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = SettingWindow()
    widget.show()

    sys.exit(app.exec())
