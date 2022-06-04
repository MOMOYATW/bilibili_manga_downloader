from PySide6.QtCore import QThread, Signal
from download_thread import DownloadThread
import os
import re


class DownloadManagerThread(QThread):
    send_task_signal = Signal(dict)
    feedback_task_signal = Signal(bool, dict)
    update_task_singal = Signal(int, str, float)

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
            latest_task['progress'] = 0
            self.updateTaskInfo(latest_task_index[0])

    def updateTaskProgress(self, index, value):
        self.task_dict[index[0]][index[1]]['progress'] = value
        self.updateTaskInfo(index[0])

    def updateTaskInfo(self, manga_id):
        finished_cnt = 0
        running_cnt = 0
        pending_cnt = 0
        error_cnt = 0
        progress = 0

        for task in self.task_dict[manga_id]:
            if 'status' in self.task_dict[manga_id][task]:
                if self.task_dict[manga_id][task]['status'] == 'finished':
                    finished_cnt += 1
                    progress += 1 / (len(self.task_dict[manga_id]) - 1)
                if self.task_dict[manga_id][task]['status'] == 'running':
                    running_cnt += 1
                    progress += self.task_dict[manga_id][task]['progress'] * \
                        1 / (len(self.task_dict[manga_id]) - 1)
                if self.task_dict[manga_id][task]['status'] == 'pending':
                    pending_cnt += 1
                if self.task_dict[manga_id][task]['status'] == 'error':
                    error_cnt += 1
        if running_cnt != 0:
            status = "下载中"
        elif pending_cnt != 0:
            status = "排队中"
        elif error_cnt != 0:
            status = "下载失败，请重新添加任务"
        else:
            status = "已完成"
            progress = 1
        self.update_task_singal.emit(
            manga_id, status, progress * 100)

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
            new_manga = True

        # judge if task already exist
        for task in tasks:
            if task['id'] not in self.task_dict[manga_info['id']] or self.task_dict[manga_info['id']][task['id']]['status'] == 'error':
                self.task_dict[manga_info['id']][task['id']] = task
                self.task_dict[manga_info['id']][task['id']]['type'] = 'honpen'
                self.task_dict[manga_info['id']
                               ][task['id']]['status'] = 'pending'
                # add to queue
                self.pending_task.append([manga_info['id'], task['id']])
        for tokuten in tokutens:
            if tokuten['item']['id'] not in self.task_dict[manga_info['id']] or self.task_dict[manga_info['id']][tokuten['item']['id']]['status'] == 'error':
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']] = tokuten
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']]['type'] = 'tokuten'
                self.task_dict[manga_info['id']
                               ][tokuten['item']['id']]['status'] = 'pending'
                # add to queue
                self.pending_task.append(
                    [manga_info['id'], tokuten['item']['id']])

        self.feedback_task_signal.emit(
            new_manga, self.task_dict[manga_info['id']])
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
        self.task_dict[index[0]][index[1]]['error'] = thread.err_log
        self.task_dict[index[0]][index[1]]['status'] = 'finished' if len(
            thread.err_log) == 0 else 'error'
        print(thread.err_log)
        self.updateTaskInfo(index[0])
        self.dispatch()

    def terminate(self) -> None:
        for thread in self.running_thread:
            thread.terminate()
        return super().terminate()
