import os
from urllib import response
from PySide6.QtCore import QThread, Signal
from service import fetch_image_list, fetch_image_token, fetch_image, fetch_video
import core

class DownloadThread(QThread):
    update_signal = Signal(list, float)
    finished_signal = Signal(list)

    def __init__(self, index, download_path, task) -> None:
        super(DownloadThread, self).__init__()
        self.index = index
        self.download_path = download_path
        self.task = task
        self.err_log = []
        self.progress = 0

    def run(self):
        """ Download images to file """
        # check if download path is exist
        curr_download_folder = os.path.join(
            core.CONFIG['download_folder'], self.download_path)
        if not os.path.exists(curr_download_folder):
            os.makedirs(curr_download_folder)
        if self.task['type'] == 'honpen':
            img_list = fetch_image_list(self.index[1])
            if img_list['code'] != 0:
                # handle error
                print('获取图像列表时出错\nDetail:{}'.format(img_list['msg']))
                return

            # iterate over image list
            for i, image in enumerate(img_list['data']['images']):
                # get image token which required when downloading
                img_token = fetch_image_token([image['path']])
                if img_token['code'] != 0:
                    # handle error
                    print('获取图像token信息时出错\nDetail:{}'.format(img_token['msg']))
                    continue
                token = img_token['data'][0]['token']
                url = img_token['data'][0]['url']
                # if image already exist
                suffix = url.split('?')[
                    0].split('.')[-1]
                data_count = 0
                download_path = os.path.join(
                    curr_download_folder, "{}.{}".format(str(i).zfill(3), suffix))
                if os.path.exists(download_path):
                    data_count = os.path.getsize(download_path)

                # save image to local file
                content = fetch_image(
                    "{}?token={}".format(url, token), range_start=data_count)
                if content is None:
                    self.err_log.append([self.index, i])
                    continue
                if content.headers['content-type'] == 'text/html' or int(content.headers['content-length']) == 0:
                    self.progress += 1
                    self.update_signal.emit(
                        self.index, 1 / len(img_list['data']['images']))
                    continue
                chunk_size = 1024
                content_size = int(
                    content.headers['content-length']) + data_count
                self.progress += (data_count /
                                  content_size) if content_size > 0 else 0
                self.update_signal.emit(
                    self.index, ((data_count /
                                 content_size) if content_size > 0 else 0) / len(img_list['data']['images']))
                with open(download_path, 'ab') as file:
                    for data in content.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        self.progress += (len(data) /
                                          content_size) if content_size > 0 else 0
                        self.update_signal.emit(self.index,
                                                ((len(data) /
                                                 content_size) if content_size > 0 else 0) / len(img_list['data']['images']))
                QThread.msleep(core.CONFIG['sleep_time'])
        elif self.task['type'] == 'tokuten':
            # if tokuten is image set
            if len(self.task['item']['pic']) != 0:
                for i, image in enumerate(self.task['item']['pic']):
                    # if image already exist
                    suffix = self.task['item']['pic'][i].split('?')[
                        0].split('.')[-1]
                    data_count = 0
                    download_path = os.path.join(
                        curr_download_folder, "{}.{}".format(str(i).zfill(3), suffix))
                    if os.path.exists(download_path):
                        data_count = os.path.getsize(download_path)

                    # save image to local file
                    content = fetch_image(
                        image, range_start=data_count)
                    if content is None:
                        self.err_log.append([self.index, i])
                        continue
                    if content.headers['content-type'] == 'text/html' or content.headers['content-length'] == 0:
                        self.progress += 1
                        self.update_signal.emit(
                            self.index, 1 / len(self.task['item']['pic']))
                        continue
                    chunk_size = 1024
                    content_size = int(
                        content.headers['content-length']) + data_count
                    self.progress += (data_count /
                                      content_size) if content_size > 0 else 0
                    self.update_signal.emit(
                        self.index, ((data_count /
                                     content_size) if content_size > 0 else 0) / len(self.task['item']['pic']))
                    with open(download_path, 'ab') as file:
                        for data in content.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            self.progress += (len(data) /
                                              content_size) if content_size > 0 else 0
                            self.update_signal.emit(
                                self.index, ((len(data) /
                                             content_size) if content_size > 0 else 0) / len(self.task['item']['pic']))
                    QThread.msleep(core.CONFIG['sleep_time'])
            else:
                # currently it must be video type
                # get suffix
                suffix = self.task['item']['video']['url'].split('?')[
                    0].split('.')[-1]
                # check if already exist
                data_count = 0
                download_path = os.path.join(
                    curr_download_folder, "{}.{}".format(str(0).zfill(3), suffix))
                if os.path.exists(download_path):
                    data_count = os.path.getsize(download_path)
                content = fetch_video(
                    self.task['item']['video']['url'], data_count)
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
