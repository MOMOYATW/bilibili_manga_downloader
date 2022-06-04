from PySide6.QtCore import QThread, Signal
from service import fetch_image


class FetchThread(QThread):
    resoponse_signal = Signal(bytes)

    def __init__(self, url, cookie) -> None:
        super(FetchThread, self).__init__()
        self.cookie = cookie
        self.url = url

    def run(self):
        # safe fetch
        response = fetch_image(self.url, self.cookie)
        self.resoponse_signal.emit(response)
