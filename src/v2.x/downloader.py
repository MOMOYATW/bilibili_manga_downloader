import sys
import core
import service
from downloader_main_ui import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    """
    Main Entrance
    """
    app = QApplication(sys.argv)
    core.read_config_file()
    core.load_qss()
    core.load_resource()
    service.update_cookie()
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
