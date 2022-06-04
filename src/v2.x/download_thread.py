import os
from PySide6.QtCore import QThread, Signal
from service import fetch_image_list, fetch_image_token, fetch_image, fetch_image_size


class DownloadThread(QThread):
    update_signal = Signal(list, float)
    finished_signal = Signal(list)

    def __init__(self, index, config, download_path, task) -> None:
        super(DownloadThread, self).__init__()
        self.config = config
        self.index = index
        self.download_path = download_path
        self.task = task
        self.err_log = []

    def run(self):
        """ Download images to file """
        # check if download path is exist
        curr_download_folder = os.path.join(
            self.config['download_folder'], self.download_path)
        if not os.path.exists(curr_download_folder):
            os.makedirs(curr_download_folder)
        err_cnt = 0
        if self.task['type'] == 'honpen':
            img_list = fetch_image_list(self.index[1], self.config['cookie'])
            if img_list['code'] != 0:
                # handle error
                print('获取图像列表时出错\nDetail:{}'.format(img_list['msg']))
                return

            # iterate over image list
            for i, image in enumerate(img_list['data']['images']):
                # get image token which required when downloading
                img_token = fetch_image_token(
                    [image['path']], self.config['width'])
                if img_token['code'] != 0:
                    # handle error
                    print('获取图像token信息时出错\nDetail:{}'.format(img_token['msg']))
                    continue
                token = img_token['data'][0]['token']
                url = img_token['data'][0]['url']
                # if image already exist
                if os.path.exists(os.path.join(curr_download_folder, "{}.jpg".format(str(i).zfill(3)))):
                    # img_size = fetch_image_size("{}?token={}".format(
                    #     url, token), self.config['cookie'])
                    # file_size = os.path.getsize(os.path.join(
                    #     curr_download_folder, "{}.jpg".format(str(i).zfill(3))))
                    # if img_size == file_size:
                    #     self.update_signal.emit(
                    #         self.index, (i + 1) / len(img_list['data']['images']))
                    #     continue
                    self.update_signal.emit(
                        self.index, (i + 1 - err_cnt) / len(img_list['data']['images']))
                    continue
                # save image to local file
                content = fetch_image("{}?token={}".format(
                    url, token), self.config['cookie'])
                if content is None:
                    self.err_log.append([self.index, i])
                    err_cnt += 1
                    continue
                with open(os.path.join(curr_download_folder, "{}.jpg".format(str(i).zfill(3))), 'wb') as file:
                    file.write(content)
                self.update_signal.emit(
                    self.index, (i + 1 - err_cnt) / len(img_list['data']['images']))
                QThread.msleep(self.config['sleep_time'])
        elif self.task['type'] == 'tokuten':
            for i, image in enumerate(self.task['item']['pic']):
                # if image already exist
                if os.path.exists(os.path.join(curr_download_folder, "{}.jpg".format(str(i).zfill(3)))):
                    # img_size = fetch_image_size(image, self.config['cookie'])
                    # file_size = os.path.getsize(os.path.join(
                    #     curr_download_folder, "{}.jpg".format(str(i).zfill(3))))
                    # if img_size == file_size:
                    #     self.update_signal.emit(
                    #         self.index, (i + 1 - err_cnt) / len(self.task['item']['pic']))
                    #     continue
                    self.update_signal.emit(
                        self.index, (i + 1 - err_cnt) / len(self.task['item']['pic']))
                    continue
                # save image to local file
                content = fetch_image(image, self.config['cookie'])
                if content is None:
                    self.err_log.append([self.index, i])
                    err_cnt += 1
                    continue
                with open(os.path.join(curr_download_folder, "{}.jpg".format(str(i).zfill(3))), 'wb') as file:
                    file.write(content)
                self.update_signal.emit(
                    self.index, (i + 1 - err_cnt) / len(self.task['item']['pic']))
                QThread.msleep(self.config['sleep_time'])
        self.finished_signal.emit(self.index)
