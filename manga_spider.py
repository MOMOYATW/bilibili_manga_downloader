import requests
import argparse
import json
from http.cookies import SimpleCookie
from time import sleep
import os
from tqdm import tqdm


def get_manga_list(manga_num, cookie):
    response = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web', {
                             "ep_id": manga_num}, cookies=cookie)
    response_data = json.loads(response.text)
    if response_data["code"] != 0:
        print(response_data["msg"])
        return -1, None
    return len(response_data["data"]["images"]), response_data["data"]["images"]


def get_manga_image(base_folder, comic_title, short_title, title, manga_list, interval_seconds):
    save_folder = os.path.join(
        base_folder, '{}/{}-{}'.format(comic_title, short_title, title))
    folder = os.path.exists(save_folder)

    if not folder:
        os.makedirs(save_folder)
    else:
        files = os.listdir(save_folder)
        if len(files) >= len(manga_list):
            return

    for i, image in enumerate(tqdm(manga_list)):
        response = requests.post(
            'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web', {"urls": "[\"" + image["path"] + "\"]"})
        response_data = json.loads(response.text)
        image_token = response_data["data"][0]["token"]
        response = requests.get(response_data["data"][0]["url"] + "?token=" + image_token, headers={
                                'referer': 'https://manga.bilibili.com', 'origin': 'https://manga.bilibili.com'})

        with open(save_folder + '/{}.jpg'.format(str(i).zfill(3)), 'wb') as file:
            file.write(response.content)
        sleep(interval_seconds)  # control speed


def get_manga_detail(manga_id, cookie):
    response = requests.post(
        'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web', {"comic_id": manga_id}, cookies=cookie)
    response_data = json.loads(response.text)
    if response_data["code"] != 0:
        print(response_data["msg"])
        return -1, None
    print(response_data["data"]["title"])
    print(response_data["data"]["classic_lines"])
    return len(response_data["data"]["ep_list"]), response_data["data"]


def get_manga_images(base_folder, interval_seconds, comic_title, manga_num, short_title, title, cookie):
    if comic_title == None:
        return -1

    length, manga_list = get_manga_list(manga_num, cookie)

    print('List retrieved successfully. total pages: {}'.format(length))

    get_manga_image(base_folder, comic_title, short_title,
                    title, manga_list, interval_seconds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bilibili Manga Spider')
    parser.add_argument('manga_id')
    parser.add_argument('--base_folder', default='./')
    parser.add_argument('--interval_seconds', default=1)
    parser.add_argument('--cookie_text')
    args = parser.parse_args()
    print('arguments:', args)

    cookie_sc = SimpleCookie(args.cookie_text)
    cookie_dict = {v.key: v.value for k, v in cookie_sc.items()}

    episode_num, manga_detail = get_manga_detail(
        args.manga_id, cookie_dict)
    episode_list, comic_title = manga_detail["ep_list"], manga_detail["title"]
    for episode in episode_list:
        if episode["is_locked"]:
            print(
                '{} - {} is locked.'.format(episode['short_title'], episode['title']))
            continue
        res = get_manga_images(args.base_folder, args.interval_seconds, comic_title, episode['id'],
                               episode['short_title'], episode['title'], cookie_dict)
        if res == -1:
            print(
                '{} - {} failed.'.format(episode['short_title'], episode['title']))
        else:
            print(
                '{} - {} finished.'.format(episode['short_title'], episode['title']))
