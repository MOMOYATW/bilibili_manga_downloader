import requests
import json
from core import read_config_file

BILIBILI_MANGA_ENDPOINT = 'https://manga.bilibili.com/twirp/comic.v1.Comic/'


def fetch_manga_detail(manga_id, cookie=None):
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'ComicDetail?device=pc&platform=web', {"comic_id": manga_id}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    except json.decoder.JSONDecodeError as e:
        response_data = {'code': -1, 'msg': response.text}
    return response_data


def fetch_search_list(keyword, cookie=None):
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'Search?device=pc&platform=web', {"key_word": keyword, "page_num": 1, "page_size": 100}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data


def fetch_image_list(ep_id, cookie=None):
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'GetImageIndex?device=pc&platform=web', {"ep_id": ep_id}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data


def fetch_image_token(urls, cookie=None):
    """
    fetch image token with original size
    """
    urls = json.dumps(urls)
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'ImageToken?device=pc&platform=web', {"urls": urls}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data

# https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web
# https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web
# https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisodeBuyInfo?device=pc&platform=web
# https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web


def fetch_tokuten(comic_id, cookie=None):
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'GetComicAlbumPlus?version=41&platform=ios', {"comic_id": comic_id}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    # response_data = response

    return response_data


def fetch_image(url, range_start=0, cookie=None):
    try:
        response = requests.get(url, cookies=cookie, stream=True, timeout=10, headers={
                                "range": "bytes={}-".format(range_start)})
    except requests.exceptions.RequestException as e:
        return None
    return response


def fetch_image_size(url, cookie=None):
    try:
        response = requests.get(url, cookies=cookie, stream=True)
    except requests.exceptions.RequestException as e:
        return None
    return int(response.headers['Content-Length'])


def fetch_latest_version():
    """
    Fetch Latest Verson and Detail informations

    Returns:
      {version, detail, download_url}
    """
    try:
        response = requests.get(
            "https://api.github.com/repos/MOMOYATW/bilibili_manga_downloader/releases/latest")
        response = response.json()
    except requests.exceptions.RequestException as e:
        return {'code': -1, 'msg': e}
    return {'code': 0, 'version': response['tag_name'], 'detail': response['body'], 'download_url': response['assets'][0]['browser_download_url']}


def fetch_video(url, cookie, range_start=0, user_agent="bilibili"):
    try:
        response = requests.get(url, cookies=cookie, headers={
                                "user-agent": user_agent, "range": "bytes={}-".format(range_start)}, timeout=10, stream=True)
    except requests.exceptions.RequestException as e:
        return None
    return response


def unlock_tokuten(tokuten_id, cookie):
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'UnlockComicAlbum?version=41', {"id": tokuten_id}, cookies=cookie)
    except requests.exceptions.RequestException as e:
        return False, e
    return True, ""


if __name__ == '__main__':
    # cookie = read_config_file({"cookie": {}})
    # response = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/BuyEpisode?device=pc&platform=web', {
    #                          "buy_method": 3, "ep_id": 535464, "pay_amount": 19, "auto_pay_gold_status": 2}, cookies=cookie['cookie'])
    # print(response.text)
    pass
