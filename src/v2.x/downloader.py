import sys
from downloader_main_ui import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    """
    Main Entrance
    """
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())
