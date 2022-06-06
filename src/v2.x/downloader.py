import sys
import core
from downloader_main_ui import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    """
    Main Entrance
    """
    app = QApplication(sys.argv)
    core.read_config_file()
    core.loadQss()
    core.loadResource()
    widget = MainWindow()
    widget.show()
    core.save_config_file()
    sys.exit(app.exec())
