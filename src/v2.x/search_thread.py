import re
from PySide6.QtCore import QThread, Signal
from service import fetch_manga_detail, fetch_search_list, fetch_tokuten


class SearchThread(QThread):
    """ Parse url or keywords and search """
    msgSignal = Signal(str)
    createParseSignal = Signal(dict)
    addTaskSignal = Signal(dict)
    createResultSignal = Signal(dict)

    def __init__(self, search_content) -> None:
        super(SearchThread, self).__init__()
        self.search_content = search_content

    def run(self):
        # parse search content
        if self.search_content == "":
            return

        # case 1: https://manga.bilibili.com/detail/mc28903/
        # manga detail website
        manga_id = re.findall(
            r'manga.bilibili.com/detail/mc[0-9]*', self.search_content)
        if len(manga_id) != 0:
            manga_id = int(manga_id[0].split('/')[2][2:])

            manga_detail = fetch_manga_detail(manga_id)

            if manga_detail['code'] != 0:
                self.msgSignal.emit('搜索失败,{}'.format(manga_detail['msg']))
                return

            # issue #2 parse tokuten
            tokuten = fetch_tokuten(manga_id)
            if tokuten['code'] != 0:
                self.msgSignal.emit('特典获取失败,{}'.format(tokuten['msg']))
                tokuten['data'] = {'list': []}
            manga_detail['data']['tokuten'] = tokuten['data']['list']
            self.createParseSignal.emit(manga_detail['data'])
            return

        # case 2: https://manga.bilibili.com/mc28903/506733
        # episode website
        manga_episode_id = re.findall(
            r'manga.bilibili.com/mc[0-9]*/[0-9]*', self.search_content)

        if len(manga_episode_id) != 0:
            manga_id = int(manga_episode_id[0].split('/')[1][2:])
            episode_id = int(manga_episode_id[0].split('/')[2])

            manga_detail = fetch_manga_detail(manga_id)
            if manga_detail['code'] != 0:
                self.msgSignal.emit('搜索失败,{}'.format(manga_detail['msg']))
                return

            # find episode
            manga_data = manga_detail['data']
            episode = next(
                (item for item in manga_data['ep_list'] if item['id'] == episode_id), None)
            if episode is None:
                self.msgSignal.emit('输入链接有误')
                return
            if episode['is_locked']:
                self.msgSignal.emit('该话尚未购买')
                return
            manga_data['list'] = [episode]
            manga_data['tokuten'] = []
            self.addTaskSignal.emit(manga_data)
            return

        # case 3: 迦希大人不气馁！
        # search keyword
        # TODO: 解析结果需要处理
        keyword = self.search_content
        keyword_result = fetch_search_list(keyword)
        if keyword_result['code'] != 0:
            self.msgSignal.emit('搜索失败,{}'.format(keyword_result['msg']))
        else:
            print(keyword_result)
            self.createResultSignal.emit(keyword_result)
