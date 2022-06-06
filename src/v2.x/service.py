import urllib
import urllib3
import requests
import json
import core

BILIBILI_MANGA_ENDPOINT = 'https://manga.bilibili.com/twirp/comic.v1.Comic/'
SESSION = requests.Session()


def fetch_manga_detail(manga_id):
    """ 
    Corresponding to api 'ComicDetail'
        method:     post
        params:     {"device"}
        body:       {"comic_id"}
        cookie:     necessary

    Parameters:
        manga_id -  comic_id

    Returns:
        response data from the server
    """
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'ComicDetail?device=pc&platform=web', {"comic_id": manga_id})
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    except json.decoder.JSONDecodeError as e:
        response_data = {'code': -1, 'msg': response.text}
    return response_data


def fetch_search_list(keyword):
    """
    Corresponding to api 'Search'
        method:     post
        params:     {}
        body:       {"key_word", "page_num", "page_size"}
        cookie:     not necessary

    Parameters:
        keyword -   key_word

    Returns:
        response data from the server
    """
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'Search?device=pc&platform=web', {"key_word": keyword, "page_num": 1, "page_size": 100})
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data


def fetch_image_list(ep_id):
    """
    Corresponding to api 'GetImageIndex'
        method:     post
        params:     {"device"}
        body:       {"ep_id"}
        cookie:     necessary

    Parameters:
        ep_id -   ep_id

    Returns:
        response data from the server
    """
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'GetImageIndex?device=pc&platform=web', {"ep_id": ep_id})
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data


def fetch_image_token(urls):
    """
    Corresponding to api 'ImageToken'
        method:     post
        params:     {}
        body:       {"urls"}
        cookie:     not necessary

    Parameters:
        urls -   urls

    Returns:
        response data from the server
    """
    urls = json.dumps(urls)
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'ImageToken?device=pc&platform=web', {"urls": urls})
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}
    return response_data

# https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web
# https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisodeBuyInfo?device=pc&platform=web


def fetch_tokuten(comic_id):
    """
    Corresponding to api 'GetComicAlbumPlus'
        method:     post
        params:     {"version", "platform"}
        body:       {"comic_id"}
        cookie:     necessary

    Parameters:
        urls -   urls

    Returns:
        response data from the server
    """
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'GetComicAlbumPlus?version=41&platform=ios', {"comic_id": comic_id})
        response_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        response_data = {'code': -1, 'msg': e}

    return response_data


def fetch_image(url, range_start=0):
    """
    Fetch image from server in stream, support breakpoint resume

    Parameters:
        url         -   url
        range_start -   bytes start download, default 0

    Returns:
        stream response from the server
    """
    try:
        response = SESSION.get(url, stream=True, timeout=10, headers={
            "range": "bytes={}-".format(range_start)})
    except requests.exceptions.RequestException as e:
        return None
    return response


def fetch_video(url, range_start=0, user_agent="bilibili"):
    """
    Fetch video from server in stream, support breakpoint resume

    Parameters:
        url         -   url
        range_start -   bytes start download, default 0
        user_agent  -   user agent

    Returns:
        stream response from the server
    """
    try:
        response = SESSION.get(url, headers={
            "user-agent": user_agent, "range": "bytes={}-".format(range_start)}, timeout=10, stream=True)
    except requests.exceptions.RequestException as e:
        return None
    return response


def fetch_latest_version():
    """
    Fetch Latest Verson and Detail informations

    Returns:
      {version, detail, download_url}
    """
    try:
        response = SESSION.get(
            "https://api.github.com/repos/MOMOYATW/bilibili_manga_downloader/releases/latest")
        response = response.json()
    except requests.exceptions.RequestException as e:
        return {'code': -1, 'msg': e}
    return {'code': 0, 'version': response['tag_name'], 'detail': response['body'], 'download_url': response['assets'][0]['browser_download_url']}


def unlock_tokuten(tokuten_id):
    try:
        response = SESSION.post(
            BILIBILI_MANGA_ENDPOINT + 'UnlockComicAlbum?version=41', {"id": tokuten_id})
    except requests.exceptions.RequestException as e:
        return False, e
    return True, ""


def update_session():
    """ Apply cookie settings to SESSION """
    SESSION.cookies.update(core.CONFIG['cookie'])

    # system proxy settings will cause error
    SESSION.trust_env = False
    system_proxy = urllib.request.getproxies()
    # correct system proxy manually
    for key in system_proxy:
        system_proxy[key] = system_proxy[key].split('//')[1]
    SESSION.proxies.update(system_proxy)
    # update user config so can override if necessary
    SESSION.proxies.update(core.CONFIG['proxy'])


# https://api.bilibili.com/x/web-interface/nav
if __name__ == '__main__':
    # cookie = read_config_file({"cookie": {}})
    # response = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/BuyEpisode?device=pc&platform=web', {
    #                          "buy_method": 3, "ep_id": 535464, "pay_amount": 19, "auto_pay_gold_status": 2}, cookies=cookie['cookie'])
    # print(response.text)
    core.read_config_file()
    update_session()
    response = SESSION.get(
        'https://www.google.com', timeout=5)
    print(response.text)
