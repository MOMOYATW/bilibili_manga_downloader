import os
from PySide6.QtCore import QThread, Signal
import service
import core


class DownloadThread(QThread):
    update_signal = Signal(list, float)
    finished_signal = Signal(list)

    def __init__(self, index, download_path) -> None:
        super(DownloadThread, self).__init__()
        self.index = index
        self.download_path = download_path
        self.err_log = []

    def run(self):
        """ Download images to file """
        # check if download path is exist
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        img_list = service.fetch_image_list(self.index[1])
        if img_list['code'] != 0:
            # handle error
            print('获取图像列表时出错\nDetail:{}'.format(img_list['msg']))
            return

        # iterate over image list
        for i, image in enumerate(img_list['data']['images']):
            # get image token which required when downloading
            img_token = service.fetch_image_token([image['path']])
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
                self.download_path, "{}.{}".format(str(i).zfill(3), suffix))
            if os.path.exists(download_path):
                data_count = os.path.getsize(download_path)

            # save image to local file
            content = service.fetch_image(
                "{}?token={}".format(url, token), range_start=data_count)
            if content is None:
                self.err_log.append([self.index, i])
                continue
            if content.headers['content-type'] == 'text/html' or int(content.headers['content-length']) == 0:
                self.update_signal.emit(
                    self.index, 1 / len(img_list['data']['images']))
                continue
            chunk_size = 1024
            content_size = int(
                content.headers['content-length']) + data_count
            self.update_signal.emit(
                self.index, ((data_count /
                              content_size) if content_size > 0 else 0) / len(img_list['data']['images']))
            with open(download_path, 'ab') as file:
                for data in content.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    self.update_signal.emit(self.index,
                                            ((len(data) /
                                                content_size) if content_size > 0 else 0) / len(img_list['data']['images']))
            QThread.msleep(core.CONFIG['sleep_time'])

        self.finished_signal.emit(self.index)
