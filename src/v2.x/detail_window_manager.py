from downloader_task_detail_ui import TaskDetailWindow
from PySide6.QtCore import Signal


class DetailWindowManager():

    def __init__(self) -> None:
        self.record = {}

    def __isWindowExist(self, manga_id: str) -> bool:
        """
        Check if window is alread exist

        Parameters:
            manga_id - comic id

        Returns:
            True if it exist, else return False
        """
        return manga_id in self.record

    def createWindow(self, manga_id):
        """
        Use parse result to create window and add to manager

        Parameters:

        Returns:

        """
        if self.__isWindowExist(manga_id):
            return self.record[manga_id]
        self.record[manga_id] = TaskDetailWindow(manga_id)
        self.record[manga_id].createParseSignal.connect(
            self.createParseSignal
        )
        self.record[manga_id].closedSignal.connect(
            self.destroyWindow
        )
        self.requestTaskInListSignal(manga_id)
        self.record[manga_id].show()

    def destroyWindow(self, manga_id: str) -> None:
        """
        Delete window from manager

        Paramters:
            manga_id - comic id

        Returns:
            None
        """
        del self.record[manga_id]

    def getParseWindow(self, manga_id: str) -> TaskDetailWindow or None:
        """
        Get window from manager by manga_id

        Paramters:
            manga_id - comic id

        Returns:
            A parse result window if exist, else return None
        """
        if self.__isWindowExist(manga_id):
            return None
        else:
            return self.record[manga_id]

    def closeAll(self) -> None:
        """
        Close all the window in manager

        Parameters:

        Returns:

        """
        for window in self.record.values():
            window.closedSignal.disconnect()
            window.close()
        self.record.clear()

    def passToDetailWindow(self, dict):
        if dict == {}:
            return
        if dict['info']['id'] in self.record:
            self.record[dict['info']['id']].applyTaskInList(dict)

    def updateDetailProgress(self, dict, value):
        if dict[0] in self.record:
            self.record[dict[0]].updateProgress(dict[1], value)

    def updateDetailStatus(self, dict, value):
        if dict[0] in self.record:
            self.record[dict[0]].updateTaskStatus(dict[1], value)

    def createParseSignal(self, parse_result):
        pass

    def requestTaskInListSignal(self):
        pass
