from PySide6.QtCore import QThread, Signal
from download_thread import DownloadThread
import os
import re


class DownloadManagerThread(QThread):
    send_task_signal = Signal(dict)
    feedback_task_signal = Signal(bool, dict)
    update_task_status_signal = Signal(int, str)
    update_task_progress_signal = Signal(int, float)
    response_parse_signal = Signal(dict)
    response_detail_signal = Signal(dict)
    update_detail_progress_signal = Signal(dict, float)
    update_detail_status_signal = Signal(dict, str)

    def __init__(self, config) -> None:
        super(DownloadManagerThread, self).__init__()
        self.finished_task = []
        self.running_thread = []
        self.pending_task = []
        self.resume_task = []
        self.task_dict = {}
        self.config = config

    def dispatch(self):
        while len(self.running_thread) < self.config['max_thread_num'] and len(self.pending_task) > 0:
            latest_task_index = self.pending_task.pop(0)
            latest_task = self.task_dict[latest_task_index[0]
                                         ][latest_task_index[1]]
            manga_folder = self.task_dict[latest_task_index[0]
                                          ]['info']['title']
            manga_folder = re.sub('[\/:*?"<>|]', '_', manga_folder.strip())
            if latest_task['type'] == 'honpen':
                episode_folder = "{} - {}".format(
                    latest_task['short_title'], latest_task['title'])

            elif latest_task['type'] == 'tokuten':
                episode_folder = "{} - {}".format(
                    latest_task['item']['title'], latest_task['item']['detail']
                )
            episode_folder = re.sub('[\/:*?"<>|]', '_', episode_folder.strip())
            self.running_thread.append(DownloadThread(latest_task_index, self.config, os.path.join(
                manga_folder, episode_folder), latest_task))
            self.running_thread[-1].finished_signal.connect(
                self.removeFinishedThread)
            self.running_thread[-1].update_signal.connect(
                self.updateTaskProgress)
            self.running_thread[-1].start()
            latest_task['status'] = 'running'
            self.update_detail_status_signal.emit(latest_task_index, '下载中')
            self.task_dict[latest_task_index[0]]['info']['cnt']['running'] += 1
            self.task_dict[latest_task_index[0]
                           ]['info']['cnt']['pending'] -= 1
            self.updateTaskInfo(latest_task_index[0])

    def updateTaskProgress(self, index, value):
        self.task_dict[index[0]]['info']['progress'] += value
        self.task_dict[index[0]][index[1]]['progress'] += value
        self.update_detail_progress_signal.emit(
            index, self.task_dict[index[0]][index[1]]['progress'])
        self.update_task_progress_signal.emit(index[0],
                                              self.task_dict[index[0]]['info']['progress'] / (len(self.task_dict[index[0]]) - 1))
        self.updateTaskInfo(index[0])

    def updateTaskInfo(self, manga_id):
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
        self.update_task_status_signal.emit(
            manga_id, status)

    def createDownloadTasks(self, task_patch):
        tasks = task_patch['list']
        tokutens = task_patch['tokuten']

        manga_info = task_patch
        del manga_info['list']
        del manga_info['tokuten']
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

        self.sendTaskToDetail(manga_info['id'])
        self.updateTaskProgress(
            self.pending_task[-1], 0)
        self.dispatch()

    def removeFinishedThread(self, index):
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
        self.updateTaskInfo(index[0])
        self.dispatch()

    def terminate(self) -> None:
        for thread in self.running_thread:
            thread.terminate()
        return super().terminate()

    def sendTaskToParse(self, manga_id):
        if manga_id in self.task_dict:
            self.response_parse_signal.emit(self.task_dict[manga_id])
            return
        self.response_parse_signal.emit({})

    def sendTaskToDetail(self, manga_id):
        if manga_id in self.task_dict:
            self.response_detail_signal.emit(self.task_dict[manga_id])
            return
        self.response_detail_signal.emit({})
