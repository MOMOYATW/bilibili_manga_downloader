from downloader_task_detail_ui import TaskDetailWindow


class DetailWindowManager():

    def __init__(self) -> None:
        self.record = {}

    def __isWindowExist(self, manga_id: str) -> bool:
        """
        Check if window is alread exist

        Parameters:
            manga_id    -   comic id

        Returns:
            True if it exist, else return False
        """
        return manga_id in self.record

    def createWindow(self, manga_id: str) -> None:
        """
        Use parse result to create window and add to manager

        Parameters:
            manga_id    -   comic_id
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
        """
        self.record.pop(manga_id)

    def closeAll(self) -> None:
        """
        Close all the window in manager
        """
        for window in self.record.values():
            window.closedSignal.disconnect()
            window.close()
        self.record.clear()

    def passToDetailWindow(self, tasks_dict: dict):
        """
        Pass items in download list to detail window

        Parameters:
            tasks_dict  -   a dict with task informations about certain manga
        """
        if tasks_dict == {}:
            return

        # pass accroding to id
        if tasks_dict['info']['id'] in self.record:
            self.record[tasks_dict['info']['id']].applyTaskInList(tasks_dict)

    def updateDetailProgress(self, task_index: list, value: float):
        """
        Update progress bar in detail window

        Parameters:
            task_index  -   [manga_id, episode_id]
            value       -   task process value
        """
        if task_index[0] in self.record:
            self.record[task_index[0]].updateProgress(task_index[1], value)

    def updateDetailStatus(self, task_index: list, value: str):
        """
        Update status in detail window

        Parameters:
            task_index  -   [manga_id, episode_id]
            value       -   task status value
        """
        if task_index[0] in self.record:
            self.record[task_index[0]].updateTaskStatus(task_index[1], value)

    def createParseSignal(self, parse_result):
        """
        Signal to override
        """
        pass

    def requestTaskInListSignal(self):
        """
        Signal to override
        """
        pass

    def updateSettings(self):
        for window in self.record.values():
            window.updateSettings()
