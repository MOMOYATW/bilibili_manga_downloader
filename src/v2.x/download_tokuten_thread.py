import os
import service
import core
from download_thread import DownloadThread
from PySide6.QtCore import QThread


class DownloadTokutenThread(DownloadThread):

    def __init__(self, index, download_path, task) -> None:
        super(DownloadTokutenThread, self).__init__(index, download_path)
        self.task = task

    def run(self):
        """ Download images to file """
        # check if download path is exist
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        # if tokuten is image set
        if len(self.task['pic']) != 0:
            for i, image in enumerate(self.task['pic']):
                # if image already exist
                suffix = self.task['pic'][i].split('?')[
                    0].split('.')[-1]
                data_count = 0
                download_path = os.path.join(
                    self.download_path, "{}.{}".format(str(i).zfill(3), suffix))
                if os.path.exists(download_path):
                    data_count = os.path.getsize(download_path)

                # save image to local file
                content = service.fetch_image(
                    image, range_start=data_count)
                if content is None:
                    self.err_log.append([self.index, i])
                    continue
                if content.headers['content-type'] == 'text/html' or content.headers['content-length'] == 0:
                    self.update_signal.emit(
                        self.index, 1 / len(self.task['pic']))
                    continue
                chunk_size = 1024
                content_size = int(
                    content.headers['content-length']) + data_count
                self.update_signal.emit(
                    self.index, ((data_count /
                                  content_size) if content_size > 0 else 0) / len(self.task['pic']))
                with open(download_path, 'ab') as file:
                    for data in content.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        self.update_signal.emit(
                            self.index, ((len(data) /
                                          content_size) if content_size > 0 else 0) / len(self.task['pic']))
                QThread.msleep(core.CONFIG['sleep_time'])

        if self.task['video'] is not None and self.task['video']['url'] != "":
            # video type
            # get suffix
            suffix = self.task['video']['url'].split('?')[
                0].split('.')[-1]
            # check if already exist
            data_count = 0
            download_path = os.path.join(
                self.download_path, "{}.{}".format(str(0).zfill(3), suffix))
            if os.path.exists(download_path):
                data_count = os.path.getsize(download_path)
            content = service.fetch_video(
                self.task['video']['url'], data_count)
            if content is None:
                self.err_log.append([self.index, 0])
                return
            if content.headers['content-type'] == 'text/html':
                self.update_signal.emit(
                    self.index, 1)
                return
            chunk_size = 1024
            content_size = int(
                content.headers['content-length']) + data_count
            self.update_signal.emit(
                self.index, (data_count / content_size) if content_size > 0 else 0)
            with open(download_path, 'ab') as file:
                for data in content.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    self.update_signal.emit(
                        self.index, (len(data) / content_size) if content_size > 0 else 0)

        self.finished_signal.emit(self.index)
