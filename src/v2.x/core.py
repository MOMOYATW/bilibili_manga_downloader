import os
import json
import sys
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize

VERSION_TAG = 'v2.1.0'
DEFAULT_CONFIG = {"cookie": {},
                  "download_folder": "./",
                  "max_thread_num": 1,
                  "check_update_when_start": True,
                  "sleep_time": 1000,
                  "style": "dark.qss"}


def read_config_file() -> None:
    """
    Read configurations in file 'settings.json', if file do not exist then use default settings.

    Parameters:

    Returns:

    """
    global CONFIG
    value_dict = {}
    file = os.path.exists('./settings.json')
    if file:
        with open('./settings.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for attribute in DEFAULT_CONFIG.keys():
            if attribute in json_data:
                value_dict[attribute] = json_data[attribute]
            else:
                value_dict[attribute] = DEFAULT_CONFIG[attribute]
        CONFIG = value_dict
        return
    CONFIG = DEFAULT_CONFIG


def save_config_file() -> None:
    """
    Save CONFIG to file 'settings.json', if not exist then create one

    Paramters:

    Returns:

    """
    with open('./settings.json', 'w') as f:
        json_str = json.dumps(CONFIG, indent=4, ensure_ascii=False)
        f.write(json_str)


def loadQss():
    global QSS
    # fetch style sheet path
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = "./"
    styleFile = os.path.join(base_path, CONFIG['style'])
    # set style sheet
    with open(styleFile, 'r') as f:
        QSS = f.read()


def loadResource():
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
