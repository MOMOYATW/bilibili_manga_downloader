import re
import sys
from core import *
from time import sleep
from settings_ui import SettingWindow
from downloader_base_ui import Ui_MainWindow
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QListWidgetItem, QMessageBox


class DownloadThread(QThread):
    progress_changed = Signal(int)
    message = Signal(QMessageBox.Icon, str, str)

    def __init__(self, window) -> None:
        super(DownloadThread, self).__init__()
        self.window = window
        self.stop = False
        self.progress_changed.connect(self.window.ui.progressBar.setValue)
        self.message.connect(self.window.pop_msg_box)

    def run(self) -> None:
        progress_value = 0
        self.progress_changed.emit(progress_value)
        download_sets = []
        for i in range(self.window.ui.listWidget.count()):
            item = self.window.ui.listWidget.item(i)
            widget = self.window.ui.listWidget.itemWidget(item)
            if widget.isChecked():
                download_sets.append(self.window.episode_list[i])
        for i, download in enumerate(download_sets):
            base_value = i / len(download_sets) * 100
            delta_value = 1 / len(download_sets) * 100
            save_folder = os.path.join(self.window.base_folder, self.window.ui.manga_title.text(),
                                       '{} - {}'.format(download['short_title'], download['title']))
            folder = os.path.exists(save_folder)
            if not folder:
                os.makedirs(save_folder)
            try:
                length, images_list = get_images_list(
                    download['id'], self.window.cookie)
            except Exception as e:
                self.message.emit(QMessageBox.Critical, '错误',
                                  '在获取 {} - {} 的图片列表时抛出异常：\n'.format(download['short_title'], download['title']) + str(e) + '\n请检查网络或代理配置')
                continue

            if length == -1:
                self.message.emit(QMessageBox.Critical, '错误', '在获取 {} - {} 的图片列表时出现错误：\n'.format(
                    download['short_title'], download['title']) + images_list)
                continue

            for i, image in enumerate(images_list):
                progress_value = base_value + \
                    delta_value * ((i + 1) / len(images_list))
                self.progress_changed.emit(progress_value)
                if self.stop:
                    break
                try:
                    res = download_episode_image(save_folder, image['path'], i)
                except Exception as e:
                    self.message.emit(QMessageBox.Critical,
                                      '错误', '在下载 {} - {} 的第{}张图片时抛出异常：\n'.format(download['short_title'], download['title'], i) + str(e) + '\n请检查网络或代理配置')
                    continue
                if res:
                    sleep(self.window.interval_seconds)  # control speed

            if self.stop:
                self.stop = False
                return

        self.progress_changed.emit(100)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.title = '哔哩哔哩漫画下载器 V1.1.2'
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.btn_close.clicked.connect(self.save_and_close)
        self.ui.btn_min.clicked.connect(self.showMinimized)
        self.ui.btn_max.clicked.connect(self.showMax)
        self.setMouseTracking(True)
        self.isPressed = False
        self.isDrag = False
        self.padding = 3
        self.direction = None
        self.ui.progressBar.setValue(0)
        self.ui.btn_getinfo.clicked.connect(self.get_manga_info)
        self.ui.btn_startdownload.clicked.connect(self.start_download)
        self.ui.btn_selectall.clicked.connect(self.select_all)
        self.ui.btn_cancelall.clicked.connect(self.cancel_all)

        self.is_downloading = False

        file = os.path.exists('./settings.json')
        if file:
            with open('./settings.json', 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            self.cookie_text = json_data['cookie_text']
            self.base_folder = json_data['base_folder']
            self.interval_seconds = json_data['interval_seconds']
        else:
            self.cookie_text = ""
            self.base_folder = './'
            self.interval_seconds = 1

        self.ui.btn_moresettings.clicked.connect(self.show_settings)

        self.cookie = parse_cookie_text(self.cookie_text)
        if self.cookie == {}:
            self.ui.label.setText(self.title + ' - 尚未设置cookie')
        else:
            self.ui.label.setText(self.title + ' - 已设置cookie')

    def showMax(self):
        if self.isMaximized() == True:
            self.showNormal()
            self.move(self.restorePos)
            self.resize(self.restoreSize)
        else:
            self.restoreSize = self.size()
            self.restorePos = self.pos()
            self.showMaximized()

    def mousePressEvent(self, QMouseEvent):
        """
        only can be drag when using left button and click the bar
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.ui.title_bar.height():
            self.isPressed = True
            self.startMovePosition = QMouseEvent.globalPos()
            self.startMousePosition = QMouseEvent.pos()

        if QMouseEvent.button() == Qt.MouseButton.LeftButton and (QMouseEvent.x() <= self.padding or self.size().width() - QMouseEvent.x() <= self.padding or QMouseEvent.y() <= self.padding or self.size().height() - QMouseEvent.y() <= self.padding):
            self.isDrag = True
            self.btnY = self.pos().y() + self.size().height() - self.minimumHeight()
            self.rightX = self.pos().x() + self.size().width() - self.minimumWidth()

    def mouseDoubleClickEvent(self, QMouseEvent):
        """
        double click to maximum and minimum the window
        """
        if QMouseEvent.button() == Qt.MouseButton.LeftButton and QMouseEvent.y() <= self.ui.title_bar.height():
            self.showMax()

    def mouseReleaseEvent(self, QMouseEvent):
        """
        release the button
        """
        self.isPressed = False
        self.isDrag = False

    def mouseMoveEvent(self, QMouseEvent):
        """
        drag custom title bar
        """
        if self.isMaximized() == False and not self.isDrag:
            if QMouseEvent.x() <= self.padding and QMouseEvent.y() <= self.padding:
                """
                left top
                """
                self.setCursor(Qt.SizeFDiagCursor)
                self.direction = 'lt'
            elif QMouseEvent.x() <= self.padding and self.size().height() - QMouseEvent.y() <= self.padding:
                """
                left bottom
                """
                self.setCursor(Qt.SizeBDiagCursor)
                self.direction = 'lb'
            elif self.size().width() - QMouseEvent.x() <= self.padding and QMouseEvent.y() <= self.padding:
                """
                right top
                """
                self.setCursor(Qt.SizeBDiagCursor)
                self.direction = 'rt'
            elif self.size().width() - QMouseEvent.x() <= self.padding and self.size().height() - QMouseEvent.y() <= self.padding:
                """
                right bottom
                """
                self.setCursor(Qt.SizeFDiagCursor)
                self.direction = 'rb'
            elif QMouseEvent.x() <= self.padding:
                """
                left
                """
                self.setCursor(Qt.SizeHorCursor)
                self.direction = 'l'
            elif self.size().width() - QMouseEvent.x() <= self.padding:
                """
                right
                """
                self.setCursor(Qt.SizeHorCursor)
                self.direction = 'r'
            elif QMouseEvent.y() <= self.padding:
                """
                top
                """
                self.setCursor(Qt.SizeVerCursor)
                self.direction = 't'
            elif self.size().height() - QMouseEvent.y() <= self.padding:
                """
                bottom
                """
                self.setCursor(Qt.SizeVerCursor)
                self.direction = 'b'
            else:
                self.direction = None
                self.setCursor(Qt.ArrowCursor)

        if self.isDrag:
            curr_size = self.size()
            curr_pos = self.pos()
            if self.direction == 'l':
                curr_size.setWidth(
                    max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                curr_pos.setX(min(curr_pos.x() + QMouseEvent.x(),
                              self.rightX))
                self.resize(curr_size)
                self.move(curr_pos)
            elif self.direction == 'r':
                curr_size.setWidth(
                    max(QMouseEvent.x(), self.minimumWidth()))
                self.resize(curr_size)
            elif self.direction == 't':
                curr_size.setHeight(
                    max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                curr_pos.setY(min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                self.resize(curr_size)
                self.move(curr_pos)
            elif self.direction == 'b':
                curr_size.setHeight(
                    max(QMouseEvent.y(), self.minimumHeight()))
                self.resize(curr_size)
            elif self.direction == 'lt':
                curr_size.setWidth(
                    max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                curr_size.setHeight(
                    max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                curr_pos.setX(min(curr_pos.x() + QMouseEvent.x(), self.rightX))
                curr_pos.setY(min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                self.resize(curr_size)
                self.move(curr_pos)
            elif self.direction == 'lb':
                curr_size.setWidth(
                    max(curr_size.width() - QMouseEvent.x(), self.minimumWidth()))
                curr_size.setHeight(
                    max(QMouseEvent.y(), self.minimumHeight()))
                curr_pos.setX(min(curr_pos.x() + QMouseEvent.x(),
                              self.rightX))
                self.resize(curr_size)
                self.move(curr_pos)
            elif self.direction == 'rt':
                curr_size.setHeight(
                    max(curr_size.height() - QMouseEvent.y(), self.minimumHeight()))
                curr_size.setWidth(
                    max(QMouseEvent.x(), self.minimumWidth()))
                curr_pos.setY(min(curr_pos.y() + QMouseEvent.y(), self.btnY))
                self.resize(curr_size)
                self.move(curr_pos)
            elif self.direction == 'rb':
                curr_size.setWidth(
                    max(QMouseEvent.x(), self.minimumWidth()))
                curr_size.setHeight(
                    max(QMouseEvent.y(), self.minimumHeight()))
                self.resize(curr_size)
            else:
                raise('Unexpected Error')
            return

        if self.isPressed:
            if self.isMaximized() == True:
                """
                when window is maximum
                restore the window size and maintain the mouse relative position
                """
                self.showNormal()
                # calculate mouse position rate
                pos_rate = QMouseEvent.x() / self.size().width()
                # calculate the distance from left to mouse
                normal_pos = self.restoreSize.width() * pos_rate
                # set the mouse position
                mouse_pos = QMouseEvent.pos()
                mouse_pos.setX(normal_pos)
                # resize the window
                self.resize(self.restoreSize)
                # calculate the window global position
                final_pos = QMouseEvent.globalPos()
                final_pos.setX(final_pos.x() - normal_pos)
                self.move(final_pos)
                self.startMovePosition = QMouseEvent.globalPos()
                self.startMousePosition = mouse_pos
            MovePos = QMouseEvent.globalPos()
            self.move(MovePos - self.startMousePosition)
            self.startMovePosition = MovePos

    def get_manga_info(self):
        """
        Get manga informations
        """
        website = self.ui.website_input.text()
        pattern = r'mc[0-9]*'
        manga_id = re.findall(pattern, website)
        if len(manga_id) == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '注意', '输入的网址无效')
            msg_box.exec_()
            return
        else:
            manga_id = manga_id[0]
        manga_id = int(manga_id[2:])
        print(manga_id)
        try:
            episode_num, manga_detail = get_manga_detail(manga_id, self.cookie)
        except Exception as e:
            msg_box = QMessageBox(QMessageBox.Critical,
                                  '错误', '获取漫画信息时触发异常:\n' + str(e) + '\n请检查网络或代理配置')
            msg_box.exec_()
            return
        if episode_num == -1:
            msg_box = QMessageBox(QMessageBox.Critical,
                                  '错误', '获取漫画信息时出现错误:\n' + str(manga_detail))
            msg_box.exec_()
            return
        self.ui.manga_title.setText(manga_detail['title'])
        self.ui.manga_author.setText(str(manga_detail['author_name']))
        self.ui.manga_description.setText(manga_detail['classic_lines'])
        self.episode_list = manga_detail['ep_list']
        self.ui.listWidget.clear()
        for episode in self.episode_list:
            if episode['title'].strip() == "":
                episode['title'] = episode['short_title']
            item = QListWidgetItem()
            checkbox = QCheckBox(
                '{} - {}'.format(episode['short_title'], episode['title']))
            if episode['is_locked']:
                checkbox.setStyleSheet('color:#707a8c;')
                checkbox.setCheckable(False)
            else:
                checkbox.setStyleSheet('color:#cccac2;')
                checkbox.setCheckable(True)
            self.ui.listWidget.addItem(item)
            self.ui.listWidget.setItemWidget(item, checkbox)

    def start_download(self):
        if not self.is_downloading:
            self.thread = DownloadThread(self)
            self.thread.finished.connect(self.download_finished)
            self.thread.started.connect(self.download_started)
            self.thread.start()
        else:
            self.thread.stop = True
            self.ui.btn_startdownload.setEnabled(False)

    def download_started(self):
        self.is_downloading = True
        self.ui.btn_getinfo.setEnabled(False)
        self.ui.btn_startdownload.setText('停止下载')

    def download_finished(self):
        self.is_downloading = False
        self.ui.btn_getinfo.setEnabled(True)
        self.ui.btn_startdownload.setText('开始下载')
        self.ui.btn_startdownload.setEnabled(True)

    def select_all(self):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            widget = self.ui.listWidget.itemWidget(item)
            if not self.episode_list[i]['is_locked']:
                widget.setChecked(True)

    def cancel_all(self):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            widget = self.ui.listWidget.itemWidget(item)
            widget.setChecked(False)

    def get_settings(self):
        self.cookie_text = self.setting_ui.ui.cookie_input.text()
        self.cookie = parse_cookie_text(self.cookie_text)
        if self.cookie == {}:
            self.ui.label.setText(self.title + ' - 尚未设置cookie')
        else:
            self.ui.label.setText(self.title + ' - 已设置cookie')
        self.base_folder = self.setting_ui.ui.path_input.text()
        self.interval_seconds = self.setting_ui.ui.spinBox.value()
        self.setting_ui.close()
        print(self.cookie, self.base_folder, self.interval_seconds)

    def show_settings(self):
        self.setting_ui = SettingWindow()
        self.setting_ui.ui.cookie_input.setText(self.cookie_text)
        self.setting_ui.ui.path_input.setText(self.base_folder)
        self.setting_ui.ui.spinBox.setValue(self.interval_seconds)

        self.setting_ui.ui.btn_close.clicked.connect(self.get_settings)
        self.setting_ui.show()

    def save_and_close(self):
        if self.is_downloading:
            msg_box = QMessageBox(
                QMessageBox.Warning, '注意', '下载仍在进行，确定要退出吗？', QMessageBox.Yes | QMessageBox.No)
            ret = msg_box.exec()

            if ret == QMessageBox.No:
                return
            self.thread.stop = True
            self.thread.finished.connect(self.close)
            return
        save = {"cookie_text": self.cookie_text,
                "base_folder": self.base_folder, "interval_seconds": self.interval_seconds}
        print(str(save))
        with open('./settings.json', 'w') as f:
            json_str = json.dumps(save, indent=4, ensure_ascii=False)
            f.write(json_str)
        self.close()

    def pop_msg_box(self, type, title, content):
        msg_box = QMessageBox(type, title, content)
        msg_box.exec()


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())
