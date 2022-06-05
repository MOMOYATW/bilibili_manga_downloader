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

        response = fetch_image(self.url, cookie=self.cookie)
        if response is None:
            self.resoponse_signal.emit(b"")
            return
        chunk_size = 1024
        content = b""
        for data in response.iter_content(chunk_size=chunk_size):
            content += data
        self.resoponse_signal.emit(content)
