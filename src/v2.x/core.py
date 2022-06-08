import os
import json
import sys
import re
import sources_rc
from PySide6.QtGui import QPixmap, QIcon, QFontDatabase
from PySide6.QtCore import QSize
from dot_dict import DotDict

VERSION_TAG = 'v2.1.2'
STYLE_CHOICE = {'light.qss': '亮色主题', 'dark.qss': '暗色主题'}
DEFAULT_CONFIG = {"cookie": {},
                  "download_folder": "./",
                  "max_thread_num": 1,
                  "check_update_when_start": True,
                  "sleep_time": 1000,
                  "style": "dark.qss",
                  "proxy": {},
                  "path_format": '{manga.title}/{episode.short_title} - {episode.title}',
                  "tokuten_path_format": '{manga.title}/{tokuten.title} - {tokuten.detail}',
                  "style_change_with_system": True}


def read_config_file() -> None:
    """
    Read configurations in file 'settings.json', if file do not exist then use default settings.
    """
    global CONFIG
    CONFIG = {}
    file = os.path.exists('./settings.json')
    if file:
        with open('./settings.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config.update(json_data)
        set_config(config)
        return
    CONFIG = DEFAULT_CONFIG


def save_config_file() -> None:
    """
    Save CONFIG to file 'settings.json', if not exist then create one
    """
    with open('./settings.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(CONFIG, indent=4, ensure_ascii=False)
        f.write(json_str)


def load_qss():
    """
    Load qss from file in config
    """
    global QSS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = "./"
    QFontDatabase.addApplicationFont(
        os.path.join(base_path, 'styles', "微软雅黑.ttf"))
    QFontDatabase.addApplicationFont(
        os.path.join(base_path, 'styles', "Montserrat.otf"))
    styleFile = os.path.join(base_path, 'styles', CONFIG['style'])
    # set style sheet
    with open(styleFile, 'r', encoding='utf-8') as f:
        QSS = f.read()


def load_resource():
    """
    Load resources to QObjects
    """
    global RESOURCE
    RESOURCE = {}
    RESOURCE['cover'] = {}
    RESOURCE["logo_pixmap"] = QPixmap(u":/imgs/icon.png")
    RESOURCE["logo_icon"] = QIcon()
    RESOURCE["logo_icon"].addFile(
        u":/imgs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["close_icon"] = QIcon()
    RESOURCE["close_icon"].addFile(
        u":/imgs/close.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["minimize_icon"] = QIcon()
    RESOURCE["minimize_icon"].addFile(
        u":/imgs/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["maximize_icon"] = QIcon()
    RESOURCE["maximize_icon"].addFile(
        u":/imgs/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["restore_icon"] = QIcon()
    RESOURCE["restore_icon"].addFile(
        u":/imgs/windowed.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["search_icon"] = QIcon()
    RESOURCE["search_icon"].addFile(
        u":/imgs/search.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["settings_icon"] = QIcon()
    RESOURCE["settings_icon"].addFile(
        u":/imgs/settings.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["play_icon"] = QIcon()
    RESOURCE["play_icon"].addFile(
        u":/imgs/start.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["pause_icon"] = QIcon()
    RESOURCE["pause_icon"].addFile(
        u":/imgs/pause.png", QSize(), QIcon.Normal, QIcon.Off)
    RESOURCE["open_icon"] = QIcon()
    RESOURCE["open_icon"].addFile(
        u":/imgs/open.png", QSize(), QIcon.Normal, QIcon.Off)


def legalize_filename(filename: str):
    """
    According to windows policy, convert illegal file name to legal file name
    """
    return re.sub('[\/:*?"<>|]', '_', filename.strip())[:255]


def generate_download_path(manga, episode):
    """
    Generate download path according to config file
    """
    path_format = CONFIG['path_format']
    manga = DotDict(manga)
    episode = DotDict(episode)
    # catch exceptions
    try:
        download_path = eval("f'{}'".format(path_format))
    except Exception as e:
        download_path = eval("f'{}'".format(DEFAULT_CONFIG['path_format']))
        set_config(
            {"path_format": DEFAULT_CONFIG['path_format']})

    legalize_path = CONFIG['download_folder']
    for path in os.path.split(download_path):
        legalize_path = os.path.join(legalize_path, legalize_filename(path))
    return legalize_path


def generate_tokuten_download_path(manga, tokuten):
    """
    Generate tokuten download path according to config file
    """
    path_format = CONFIG['tokuten_path_format']
    manga = DotDict(manga)
    tokuten = DotDict(tokuten)
    # catch exceptions
    try:
        download_path = eval("f'{}'".format(path_format))
    except Exception as e:
        download_path = eval("f'{}'".format(
            DEFAULT_CONFIG['tokuten_path_format']))
        set_config(
            {"tokuten_download_format": DEFAULT_CONFIG['tokuten_path_format']})

    legalize_path = CONFIG['download_folder']
    for path in os.path.split(download_path):
        legalize_path = os.path.join(legalize_path, legalize_filename(path))
    return legalize_path


def set_config(settings: dict) -> None:
    """
    Set CONFIG
    """
    global CONFIG
    for setting in settings:
        if setting in DEFAULT_CONFIG:
            if setting == "download_folder" and not os.path.exists(settings[setting]):
                settings[setting] = DEFAULT_CONFIG["download_folder"]
                print('下载路径已重置')
            if setting == "path_format":
                exps = re.findall(r'{.*?}', settings[setting])
                for exp in exps:
                    res = re.findall(
                        r'^{episode\..*?}$|^{manga\..*?}$', exp)
                    if len(res) == 0:
                        # use default config
                        settings[setting] = DEFAULT_CONFIG['path_format']
                        print('路径格式已重置')
                        break
            if setting == "tokuten_path_format":
                exps = re.findall(r'{.*?}', settings[setting])
                for exp in exps:
                    res = re.findall(
                        r'^{tokuten\..*?}$|^{manga\..*?}$', exp)
                    if len(res) == 0:
                        # use default config
                        settings[setting] = DEFAULT_CONFIG['tokuten_path_format']
                        print('特典路径格式已重置')
                        break

            CONFIG[setting] = settings[setting]
    load_qss()
    load_resource()


if __name__ == '__main__':
    pass
