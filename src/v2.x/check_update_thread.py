from PySide6.QtCore import QThread, Signal
import service
import core


class CheckUpdateThread(QThread):
    """ Thread for checking update """
    result_signal = Signal(bool, dict)
    # false means failed or no need to update, dict save msg
    # true means success, dict save new version information

    def __init__(self, ) -> None:
        super(CheckUpdateThread, self).__init__()

    def run(self):
        latest_info = service.fetch_latest_version()
        if latest_info['code'] != 0:
            self.result_signal.emit(
                False, {"msg": "查询更新失败,\n{}".format(latest_info['msg'])})
            return
        if latest_info['version'] != core.VERSION_TAG:
            self.result_signal.emit(True, latest_info)
            return
        self.result_signal.emit(False, {"msg": "已是最新版本"})
