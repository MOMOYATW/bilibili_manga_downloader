from downloader_parse_ui import ParseResultWindow


class ParseWindowManager():
    def __init__(self, resource, qss) -> None:
        self.record = {}
        self.resource = resource
        self.qss = qss

    def __isWindowExist(self, manga_id: str) -> bool:
        """
        Check if window is alread exist

        Parameters:
            manga_id - comic id

        Returns:
            True if it exist, else return False
        """
        return manga_id in self.record

    def createWindow(self, parse_result: dict) -> ParseResultWindow:
        """
        Use parse result to create window and add to manager

        Parameters:
            parse_result - parse result fetch from server

        Returns:
            A parse result window which created by parse_result
        """
        if self.__isWindowExist(parse_result['id']):
            return self.record[parse_result['id']]
        self.record[parse_result['id']] = ParseResultWindow(
            parse_result, self.resource, self.qss)
        self.record[parse_result['id']].closedSignal.connect(
            self.destroyWindow)
        return self.record[parse_result['id']]

    def destroyWindow(self, manga_id: str) -> None:
        """
        Delete window from manager

        Paramters:
            manga_id - comic id

        Returns:
            None
        """
        del self.record[manga_id]

    def getParseWindow(self, manga_id: str) -> ParseResultWindow or None:
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
