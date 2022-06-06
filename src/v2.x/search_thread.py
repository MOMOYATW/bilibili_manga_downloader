import re
from PySide6.QtCore import QThread, Signal
from service import fetch_manga_detail, fetch_search_list, fetch_tokuten


class SearchThread(QThread):
    message_signal = Signal(str)
    episodes_result_signal = Signal(dict)
    single_result_signal = Signal(dict)
    keyword_result_signal = Signal(dict)

    def __init__(self, search_content) -> None:
        super(SearchThread, self).__init__()
        self.search_content = search_content

    def run(self):
        # parse search content
        print(self.search_content)
        if self.search_content == "":
            self.message_signal.emit('搜索不可为空')
            return
        # case 1: https://manga.bilibili.com/detail/mc28903/
        # manga website
        manga_id = re.findall(
            r'manga.bilibili.com/detail/mc[0-9]*', self.search_content)
        if len(manga_id) != 0:
            manga_id = int(manga_id[0].split('/')[2][2:])
            manga_detail = fetch_manga_detail(manga_id)
            if manga_detail['code'] != 0:
                self.message_signal.emit('搜索失败,{}'.format(manga_detail['msg']))
                manga_detail['data'] = {}
                return

            # issue #2 parse tokuten
            tokuten = fetch_tokuten(manga_id)
            if tokuten['code'] != 0:
                self.message_signal.emit('特典获取失败,{}'.format(tokuten['msg']))
                tokuten['data'] = {'list': []}
            manga_detail['data']['tokuten'] = tokuten['data']['list']
            self.episodes_result_signal.emit(manga_detail['data'])
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
                self.message_signal.emit('搜索失败,{}'.format(manga_detail['msg']))
            # find episode
            manga_data = manga_detail['data']
            list = []
            for i in range(len(manga_data['ep_list'])):
                if manga_data['ep_list'][i]['id'] == episode_id:
                    list.append(manga_data['ep_list'][i])
            if len(list) == 0:
                self.message_signal.emit('输入链接有误')
                return
            if list[0]['is_locked']:
                self.message_signal.emit('该话尚未购买')
                return
            manga_data.pop('ep_list')
            manga_data['list'] = list
            self.single_result_signal.emit(manga_data)
            return
        # case 3: 迦希大人不气馁！
        # search keyword
        keyword = self.search_content
        keyword_result = fetch_search_list(keyword)
        if keyword_result['code'] != 0:
            self.message_signal.emit('搜索失败,{}'.format(keyword_result['msg']))
        else:
            self.keyword_result_signal.emit(keyword_result)
