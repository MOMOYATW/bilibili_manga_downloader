import os
import re
import json
import img2pdf
import requests
from http.cookies import SimpleCookie

BILIBILI_MANGA_ENDPOINT = 'https://manga.bilibili.com/twirp/comic.v1.Comic/'
VERSION_TAG = 'v1.4.1'


def fetch_images_list(episode_id, cookie):
    """
    Get the images list of certain episode

    Parameters:
      episode_id - the num code of certain episode
      cookie    - cookie contains SESSDATA

    Returns:
      the length of images list and the list itself
      if failed, returns -1 with error message

    Raise:
      Exception
    """
    try:
        response = requests.post(BILIBILI_MANGA_ENDPOINT + 'GetImageIndex?device=pc&platform=web', {
            "ep_id": episode_id}, cookies=cookie)
    except Exception as e:
        raise(e)
    response_data = json.loads(response.text)
    if response_data["code"] != 0:
        return -1, response_data['msg']
    return len(response_data["data"]["images"]), response_data["data"]["images"]


def get_manga_detail(manga_id, cookie):
    """
    Get the detail information of certain manga, including title, author, episode list, etc.

    Parameters:
      manga_id - the num code of certain manga
      cookie   - cookie contains SESSDATA

    Returns:
      the length of episode list and manga detail informations
      if failed, returns -1 with error message

    Raise:
      Exception
    """
    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'ComicDetail?device=pc&platform=web', {"comic_id": manga_id}, cookies=cookie)
    except Exception as e:
        raise(e)
    response_data = json.loads(response.text)
    if response_data["code"] != 0:
        return -1, response_data["msg"]
    return len(response_data["data"]["ep_list"]), response_data["data"]


def download_episode_image(download_path, image_url, index):
    """
    Save the image to download_path

    Parameters:
      download_path - the path saves the image
      image_url     - the url to request image
      index         - the index of current downloading image

    Returns:
      success returns True, failed returns False

    Raise:
      Exception
    """
    folder = os.path.exists(download_path)
    if not folder:
        os.makedirs(download_path)

    image_path = os.path.join(
        download_path, '{}.jpg'.format(str(index).zfill(3)))

    image = os.path.exists(image_path)
    if image:
        return False

    try:
        response = requests.post(
            BILIBILI_MANGA_ENDPOINT + 'ImageToken?device=pc&platform=web', {"urls": "[\"" + image_url + "\"]"})
    except Exception as e:
        raise(e)
    response_data = json.loads(response.text)
    image_token = response_data["data"][0]["token"]
    response = requests.get(response_data["data"][0]["url"] + "?token=" + image_token, headers={
                            'referer': 'https://manga.bilibili.com', 'origin': 'https://manga.bilibili.com'})

    with open(image_path, 'wb') as file:
        file.write(response.content)
    return True


def parse_cookie_text(cookie_text):
    """
    Convert cookie_text into cookie object

    Parameters:
      cookie_text - cookie in string type

    Returns:
      cookie object
    """
    cookie_sc = SimpleCookie(cookie_text)
    cookie = {v.key: v.value for k, v in cookie_sc.items()}
    return cookie


def read_config_file(attributes_dict: dict) -> dict:
    """
    Read configurations in file 'settings.json', if file do not exist then return default settings.

    Parameters:
      attributes_dict    - attributes need to read out, with default value

    Returns:
      Attributes value ordered in dict, or default value when not exist
    """
    value_dict = {}
    file = os.path.exists('./settings.json')
    if file:
        with open('./settings.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for attribute in attributes_dict.keys():
            if attribute in json_data:
                value_dict[attribute] = json_data[attribute]
            else:
                value_dict[attribute] = attributes_dict[attribute]
        return value_dict
    return attributes_dict


def parse_website(website):
    """
    Parse website to get manga id

    Parameters:
      website - bilibili manga website, eg. https://manga.bilibili.com/detail/mc28560?from=manga_homepage

    Returns:
      manga id, if parsed failed returns -1
    """
    manga_id = re.findall(r'mc[0-9]*', website)
    if len(manga_id) == 0:
        return -1
    else:
        manga_id = manga_id[0]
    return int(manga_id[2:])


def convert_images_to_pdf(download_path, savefile_path):
    """
    Convert images to a pdf file

    Parameters:
      download_path - images path
      savefile_path - name of the pdf to save (with .pdf)

    Returns:

    """
    with open(savefile_path, "wb") as f:
        f.write(img2pdf.convert(
            [i for i in os.listdir(download_path) if i.endswith('.jpg')]))


def fetch_latest_version():
    """
    Fetch Latest Verson and Detail informations

    Returns:
      [version, detail]
    """
    response = requests.get(
        "https://api.github.com/repos/MOMOYATW/bilibili_manga_downloader/releases/latest")
    response = response.json()
    return {'version': response['tag_name'], 'detail': response['body'], 'download_url': response['assets'][0]['browser_download_url']}


if __name__ == '__main__':
    print(read_config_file(
        {"cookie_text": "", "base_folder": "./", "interval_seconds": 1000}))
