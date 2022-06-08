from PySide6.QtCore import QThread, Signal
from download_thread import DownloadThread
from download_tokuten_thread import DownloadTokutenThread
import core


class DownloadManagerThread(QThread):
    feedback_task_signal = Signal(bool, dict)
    update_task_status_signal = Signal(int, str)
    update_task_progress_signal = Signal(int, float)
    response_parse_signal = Signal(dict)
    response_detail_signal = Signal(dict)
    update_detail_progress_signal = Signal(dict, float)
    update_detail_status_signal = Signal(dict, str)

    def __init__(self) -> None:
        super(DownloadManagerThread, self).__init__()
        self.finished_task = []
        self.running_thread = []
        self.pending_task = []
        self.resume_task = []
        self.task_dict = {}

    def dispatch(self):
        """
        Dispatch download threads
        called when a thread finished, or a task created
        """
        while len(self.running_thread) < core.CONFIG['max_thread_num'] and len(self.pending_task) > 0:
            # get the first task in pending queue
            latest_task_index = self.pending_task.pop(0)
            latest_task = self.task_dict[latest_task_index[0]
                                         ][latest_task_index[1]]

            # construct download path

            if latest_task['type'] == 'honpen':
                download_path = core.generate_download_path(
                    self.task_dict[latest_task_index[0]]['info'], latest_task)
                thread = DownloadThread(latest_task_index, download_path)
            elif latest_task['type'] == 'tokuten':
                download_path = core.generate_tokuten_download_path(
                    self.task_dict[latest_task_index[0]]['info'], latest_task['item'])
                thread = DownloadTokutenThread(
                    latest_task_index, download_path, latest_task['item'])

            # create thread and append to list
            self.running_thread.append(thread)
            self.running_thread[-1].finished_signal.connect(
                self.removeFinishedThread)
            self.running_thread[-1].update_signal.connect(
                self.updateTaskProgress)
            self.running_thread[-1].start()

            # update status
            latest_task['status'] = 'running'
            self.update_detail_status_signal.emit(latest_task_index, '下载中')

            # update statistic info
            self.task_dict[latest_task_index[0]]['info']['cnt']['running'] += 1
            self.task_dict[latest_task_index[0]
                           ]['info']['cnt']['pending'] -= 1
            self.updateTaskStatus(latest_task_index[0])

    def updateTaskProgress(self, index: list, value: float):
        """
        Update progress of task

        Parameters:
            index   -   [manga_id, episode_id]
            value   -   progress increased value

        """
        # update total progress and sub progress
        self.task_dict[index[0]]['info']['progress'] += value
        self.task_dict[index[0]][index[1]]['progress'] += value

        # emit signals
        self.update_detail_progress_signal.emit(
            index, self.task_dict[index[0]][index[1]]['progress'])
        self.update_task_progress_signal.emit(index[0],
                                              self.task_dict[index[0]]['info']['progress'] / (len(self.task_dict[index[0]]) - 1))
        self.updateTaskStatus(index[0])

    def updateTaskStatus(self, manga_id: str):
        """
        Update task status

        Parameters:
            manga_id    -   comic_id
        """
        # judge by statistics
        if self.task_dict[manga_id]['info']['cnt']['running'] != 0:
            status = "下载中"
        elif self.task_dict[manga_id]['info']['cnt']['pending'] != 0:
            status = "排队中"
        elif self.task_dict[manga_id]['info']['cnt']['error'] != 0:
            status = "部分任务失败"
        else:
            status = "已完成"
            self.task_dict[manga_id]['info']['progress'] = len(
                self.task_dict[manga_id]) - 1
            self.update_task_progress_signal.emit(manga_id, 1)

        # emit signal
        self.update_task_status_signal.emit(
            manga_id, status)

    def createDownloadTasks(self, task_patch: list):
        """
        Register task in manager

        Paramters:
            task_patch  -   tasks patched from parse window
        """
        tasks = task_patch['list']
        tokutens = task_patch['tokuten']
        manga_info = task_patch
        manga_info.pop('list')
        manga_info.pop('tokuten')

        new_manga = False
        # judge if manga is exist
        if manga_info['id'] not in self.task_dict:
            self.task_dict[manga_info['id']] = {}
            self.task_dict[manga_info['id']]['info'] = manga_info
            self.task_dict[manga_info['id']]['info']['progress'] = 0
            self.task_dict[manga_info['id']]['info']['cnt'] = {
                'pending': 0, 'running': 0, 'resume': 0, 'error': 0}
            new_manga = True

        # judge if task already exist
        for task in tasks:
            if task['id'] not in self.task_dict[manga_info['id']]:
                self.task_dict[manga_info['id']][task['id']] = task
                self.task_dict[manga_info['id']][task['id']]['type'] = 'honpen'
                self.task_dict[manga_info['id']][task['id']]['progress'] = 0
                self.task_dict[manga_info['id']
                               ][task['id']]['status'] = 'pending'
                self.task_dict[manga_info['id']]['info']['cnt']['pending'] += 1
                # add to queue
                self.pending_task.append([manga_info['id'], task['id']])

        for tokuten in tokutens:
            if tokuten['item']['id'] not in self.task_dict[manga_info['id']]:
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']] = tokuten
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']]['type'] = 'tokuten'
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']]['progress'] = 0
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']]['status'] = 'pending'
                self.task_dict[manga_info['id']]['info']['cnt']['pending'] += 1
                # add to queue
                self.pending_task.append(
                    [manga_info['id'], tokuten['item']['id']])

        self.feedback_task_signal.emit(
            new_manga, self.task_dict[manga_info['id']])

        # always tell detail manager
        self.sendTaskToDetail(manga_info['id'])
        self.updateTaskProgress(
            self.pending_task[-1], 0)
        self.dispatch()

    def removeFinishedThread(self, index):
        """
        After finished downloading, move thread out of list

        Paramters:
            index   -   [manga_id, episode_id]
        """
        pop_index = -1
        for i, thread in enumerate(self.running_thread):
            if thread.index == index:
                pop_index = i
        if pop_index == -1:
            print('not exist')
            return
        thread = self.running_thread.pop(pop_index)
        self.task_dict[index[0]][index[1]]['status'] = 'finished'
        self.task_dict[index[0]]['info']['cnt']['progress'] = 1
        self.task_dict[index[0]]['info']['cnt']['running'] -= 1

        if len(thread.err_log) != 0:
            self.task_dict[index[0]]['info']['cnt']['error'] += 1
            self.update_detail_status_signal.emit(index, '部分失败')
        else:
            self.update_detail_status_signal.emit(index, '已完成')
            self.update_detail_progress_signal.emit(index, 1)
        print(thread.err_log)
        self.updateTaskStatus(index[0])
        self.dispatch()

    def terminate(self) -> None:
        """
        Before terminate itself, terminate all running threads
        """
        for thread in self.running_thread:
            thread.terminate()
        return super().terminate()

    def sendTaskToParse(self, manga_id):
        """
        Send tasks to parse window

        Paramters:
            manga_id    -   comic_id
        """
        if manga_id in self.task_dict:
            self.response_parse_signal.emit(self.task_dict[manga_id])
            return
        self.response_parse_signal.emit({})

    def sendTaskToDetail(self, manga_id):
        """
        send tasks to detail windows

        Parameters:
            manga_id    -   comic_id
        """
        if manga_id in self.task_dict:
            self.response_detail_signal.emit(self.task_dict[manga_id])
            return
        self.response_detail_signal.emit({})
