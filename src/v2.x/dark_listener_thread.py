from PySide6.QtCore import QThread, Signal
import darkdetect


class DarkListenerThread(QThread):
    themeChangedSignal = Signal(str)

    def __init__(self, ) -> None:
        super(DarkListenerThread, self).__init__()

    def run(self):
        darkdetect.listener(self.themeChangedSignal.emit)
