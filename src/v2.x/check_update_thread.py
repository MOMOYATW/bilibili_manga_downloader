from PySide6.QtCore import QThread, Signal
from service import fetch_latest_version
from core import VERSION_TAG


class CheckUpdateThread(QThread):
    result_signal = Signal(bool, dict)

    def __init__(self, ) -> None:
        super(CheckUpdateThread, self).__init__()

    def run(self):
        latest_info = fetch_latest_version()
        if latest_info['code'] != 0:
            self.result_signal.emit(
                False, "查询更新失败,\n{}".format(latest_info['msg']))
            return
        if latest_info['version'] != VERSION_TAG:
            self.result_signal.emit(True, latest_info)
            return
        self.result_signal.emit(False, "已是最新版本")
