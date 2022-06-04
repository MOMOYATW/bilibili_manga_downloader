from time import sleep
import requests
import json

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


def fetch_image_token(urls, width, cookie=None):
    # add width info
    if width is not None:
        for i in range(len(urls)):
            urls[i] += "@{}w.jpg".format(width)
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
    # https://manga.bilibili.com/twirp/user.v1.User/GetMyAlbum?device=pc&platform=web
    # appkey=9f7caa979c66756d&mobi_app=ipad_comic&version=41&build=72&platform=ios&device=pad&buvid=YD4254D8C81066A34EE3ACE22425D44668CA&machine=iPad+Air+4G&access_key=302c023bccab0c30b6a0645143387d11&is_teenager=0&ts=1654225204
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'GetComicAlbumPlus?version=41', {"comic_id": comic_id}, cookies=cookie)
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    # response_data = response

    return response_data


def fetch_image(url, cookie=None):
    try:
        response = requests.get(url, cookies=cookie)
    except requests.exceptions.RequestException as e:
        return None
    return response.content


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


if __name__ == '__main__':
    pass
