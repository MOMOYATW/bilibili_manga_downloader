import sys
from core import *
from settings_ui import SettingWindow
from downloader_base_ui import Ui_MainWindow
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtWidgets import QApplication,  QCheckBox, QListWidgetItem, QMessageBox, QSizeGrip
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QPixmap, QPalette, QColor
from CustomWindow import CustomWindow
import tempfile
import sources_rc


class DownloadThread(QThread):
    progress_changed = Signal(int)
    pop_message = Signal(QMessageBox.Icon, str, str)
    sleep_thread = Signal()
    update_checkbox = Signal(int, int, int, str)
    play_music = Signal()

    def __init__(self, window) -> None:
        super(DownloadThread, self).__init__()

        self.window = window
        self.stop = False

    def run(self) -> None:
        progress_value = 0
        self.progress_changed.emit(progress_value)
        download_sets = []
        for i in range(self.window.ui.listWidget.count()):
            item = self.window.ui.listWidget.item(i)
            widget = self.window.ui.listWidget.itemWidget(item)
            if widget.isChecked():
                download_sets.append([self.window.episode_list[i], i])
        if download_sets == []:
            return
        for i, download in enumerate(download_sets):
            episode_id = download[1]
            download = download[0]
            base_value = i / len(download_sets) * 100
            delta_value = 1 / len(download_sets) * 100
            self.update_checkbox.emit(
                episode_id, 0, 0, '{} - {}'.format(download['short_title'], download['title']))

            # fixed issue #1
            # check path name
            safe_manga_title = re.sub(
                '[\/:*?"<>|]', '_', self.window.ui.manga_title.text())
            safe_filename = re.sub(
                '[\/:*?"<>|]', '_', '{} - {}'.format(download['short_title'], download['title']))
            save_folder = os.path.join(
                self.window.base_folder, safe_manga_title, safe_filename)
            folder = os.path.exists(save_folder)
            if not folder:
                os.makedirs(save_folder)
            try:
                length, images_list = fetch_images_list(
                    download['id'], self.window.cookie)
            except Exception as e:
                self.pop_message.emit(QMessageBox.Critical, '错误',
                                      '在获取 {} - {} 的图片列表时抛出异常：\n'.format(download['short_title'], download['title']) + str(e) + '\n请检查网络或代理配置')
                continue

            if length == -1:
                self.pop_message.emit(QMessageBox.Critical, '错误', '在获取 {} - {} 的图片列表时出现错误：\n'.format(
                    download['short_title'], download['title']) + images_list)
                continue

            for index, image in enumerate(images_list):
                self.update_checkbox.emit(episode_id, index, len(
                    images_list), '{} - {}'.format(download['short_title'], download['title']))
                progress_value = base_value + \
                    delta_value * ((index + 1) / len(images_list))
                self.progress_changed.emit(progress_value)
                if self.stop:
                    break
                try:
                    res = download_episode_image(
                        save_folder, image['path'], index)
                except Exception as e:
                    self.pop_message.emit(QMessageBox.Critical,
                                          '错误', '在下载 {} - {} 的第{}张图片时抛出异常：\n'.format(download['short_title'], download['title'], index) + str(e) + '\n请检查网络或代理配置')
                    continue
                if res:
                    # control speed
                    QThread.msleep(self.window.interval_seconds)

            if self.stop:
                self.stop = False
                return
            self.update_checkbox.emit(
                episode_id, -1, -1, '{} - {}'.format(download['short_title'], download['title']))
        self.progress_changed.emit(100)
        self.play_music.emit()


class MainWindow(CustomWindow):
    def __init__(self):
        super().__init__()
        self.title = '哔哩哔哩漫画下载器 V1.4.1'
        self.setWindowTitle(self.title)
        self.tempdir = tempfile.mkdtemp()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set Custom Window paramters
        self.main_widget = self.ui.background
        self.outermost_layout = self.ui.margin_layout
        self.title_bar_height = self.ui.title_bar.height()
        self.edge_scaling = False

        self.drawShadow()
        self.loadAudioFile()
        self.loadStyleSheet()

        self.is_downloading = False
        self.setting_ui = SettingWindow()
        self.ui.progressBar.setValue(0)

        self.ui.btn_min.clicked.connect(self.showMinimized)
        self.ui.btn_close.clicked.connect(self.saveAndClose)
        self.ui.btn_max.clicked.connect(self.showMaximizeOrNormalize)

        self.ui.btn_selectall.clicked.connect(self.selectAll)
        self.ui.btn_cancelall.clicked.connect(self.cancelAll)
        self.ui.btn_getinfo.clicked.connect(self.getMangaInfo)
        self.ui.btn_startdownload.clicked.connect(self.startDownload)
        self.ui.btn_moresettings.clicked.connect(self.showSettings)
        self.sizegrip = QSizeGrip(self.ui.sizegrip)

        # read out settings and parse cookie
        self.cookie_text, self.base_folder, self.interval_seconds = read_config_file(
            {"cookie_text": "", "base_folder": "./", "interval_seconds": 1000})
        self.cookie = parse_cookie_text(self.cookie_text)
        if self.cookie == {}:
            self.ui.label.setText(self.title + ' - 尚未设置cookie')
        else:
            self.ui.label.setText(self.title + ' - 已设置cookie')

    def loadAudioFile(self):
        """
        Load audio file from temp directory
        and set the player
        """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        self.audioOutput = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setSource(QUrl.fromLocalFile(os.path.join(
            base_path, "mp3", "download_finished.mp3")))

    def loadStyleSheet(self):
        """
        Load qss
        """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        styleFile = 'style.qss'
        if os.path.exists(os.path.join('.', styleFile)):
            styleFile = os.path.join('.', styleFile)
        else:
            styleFile = os.path.join(base_path, 'style', styleFile)

        with open(styleFile, 'r') as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def selectAll(self):
        """
        Select all unlocked episodes
        """
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            widget = self.ui.listWidget.itemWidget(item)
            if not self.episode_list[i]['is_locked']:
                widget.setChecked(True)

    def cancelAll(self):
        """
        Cancel all episodes
        """
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            widget = self.ui.listWidget.itemWidget(item)
            widget.setChecked(False)

    def saveAndClose(self):
        """
        Save user settings before close winodw,
        also check if is downloading then give a message box to warning
        """
        if self.is_downloading:
            msg_box = QMessageBox(
                QMessageBox.Warning, '注意', '下载仍在进行，确定要退出吗？', QMessageBox.Yes | QMessageBox.No)
            ret = msg_box.exec()

            if ret == QMessageBox.No:
                return
        # check if subwindow is showing
        if self.setting_ui and self.setting_ui.isVisible():
            self.setting_ui.close()

        save = {"cookie_text": self.cookie_text,
                "base_folder": self.base_folder, "interval_seconds": self.interval_seconds}
        with open('./settings.json', 'w') as f:
            json_str = json.dumps(save, indent=4, ensure_ascii=False)
            f.write(json_str)

        if self.is_downloading:
            self.thread.stop = True
            self.thread.finished.connect(self.close)
            return
        self.close()

    def closeEvent(self, event) -> None:
        self.saveAndClose()

    def showSettings(self):
        """
        Show Settings Window
        """
        self.setting_ui.ui.cookie_input.setText(self.cookie_text)
        self.setting_ui.ui.path_input.setText(self.base_folder)
        self.setting_ui.ui.spinBox.setValue(self.interval_seconds)
        self.setting_ui.ui.btn_save.clicked.connect(self.fetchSettings)
        self.setting_ui.show()

    def getMangaInfo(self):
        """
        Get manga informations
        """
        # parse website input
        website = self.ui.website_input.text()
        manga_id = parse_website(website)
        if manga_id == -1:
            self.popMsgBox(QMessageBox.Warning, '注意', '输入的网址无效')
            return
        # get manga detail informations
        try:
            episode_num, manga_detail = get_manga_detail(manga_id, self.cookie)
        except Exception as e:
            self.popMsgBox(QMessageBox.Critical,
                           '错误', '获取漫画信息时触发异常:\n' + str(e) + '\n请检查网络或代理配置')
            return
        if episode_num == -1:
            self.popMsgBox(QMessageBox.Critical,
                           '错误', '获取漫画信息时出现错误:\n' + str(manga_detail))
            return
        # set ui
        print(manga_detail)
        response = requests.get(manga_detail['vertical_cover'])
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.ui.cover.setPixmap(pixmap)
        self.ui.manga_title.setText(manga_detail['title'])
        self.ui.manga_author.setText(" ".join(str(i)
                                     for i in manga_detail['author_name']))
        self.ui.manga_description.setText(manga_detail['classic_lines'])
        self.ui.listWidget.clear()

        # save episode list and show in ui
        manga_detail['ep_list'].reverse()
        self.episode_list = manga_detail['ep_list']
        print(self.episode_list)
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

    def startDownload(self):
        """
        Create a new thread to download,
        advoid not responding.
        """
        if not self.is_downloading:
            self.thread = DownloadThread(self)
            self.thread.finished.connect(self.downloadFinished)
            self.thread.started.connect(self.downloadStarted)
            self.thread.progress_changed.connect(self.ui.progressBar.setValue)
            self.thread.pop_message.connect(self.popMsgBox)
            self.thread.update_checkbox.connect(self.setCheckBox)
            self.thread.play_music.connect(self.playAudio)
            self.thread.start()
        else:
            self.thread.stop = True
            self.ui.btn_startdownload.setEnabled(False)

    def downloadStarted(self):
        """
        Execute when download is started
        """
        self.is_downloading = True
        self.ui.btn_getinfo.setEnabled(False)
        self.ui.btn_startdownload.setText('停止下载')

    def downloadFinished(self):
        """
        Excute when download is finished
        """
        self.is_downloading = False
        self.ui.btn_getinfo.setEnabled(True)
        self.ui.btn_startdownload.setText('开始下载')
        self.ui.btn_startdownload.setEnabled(True)

    def fetchSettings(self):
        """
        From subwindow get informations and close it
        """
        self.cookie_text = self.setting_ui.ui.cookie_input.text()
        self.cookie = parse_cookie_text(self.cookie_text)
        if self.cookie == {}:
            self.ui.label.setText(self.title + ' - 尚未设置cookie')
        else:
            self.ui.label.setText(self.title + ' - 已设置cookie')
        self.base_folder = self.setting_ui.ui.path_input.text()
        self.interval_seconds = self.setting_ui.ui.spinBox.value()
        self.setting_ui.close()

    def popMsgBox(self, type, title, content):
        """
        Pop out a message box, maybe change messagebox ui in future
        """
        msg_box = QMessageBox(type, title, content)
        msg_box.exec()

    def setCheckBox(self, episode_id, image_id, images_num, title):
        """
        Set CheckBox value to show process
        """
        item = self.ui.listWidget.item(episode_id)
        widget = self.ui.listWidget.itemWidget(item)
        if image_id == 0 and images_num == 0:
            widget.setText(title + ' - 正在获取图片列表')
        elif image_id == -1 and images_num == -1:
            widget.setText(title + ' - 下载完成')
        else:
            widget.setText(
                title + ' - 正在下载中({}/{})'.format(image_id, images_num))

    def playAudio(self):
        self.player.stop()
        self.player.play()


if __name__ == '__main__':
    """
    create and show window
    """
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())
