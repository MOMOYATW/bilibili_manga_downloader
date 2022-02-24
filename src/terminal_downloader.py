import argparse
from core import *
from tqdm import tqdm
from time import sleep


if __name__ == '__main__':
    """
    Terminal version of bilibili manga downloader
    """
    parser = argparse.ArgumentParser(description='Bilibili Manga Downloader')
    parser.add_argument('manga_id')
    parser.add_argument('--base_folder', default='./')
    parser.add_argument('--interval_seconds', default=1)
    parser.add_argument('--cookie_text', default='')
    args = parser.parse_args()
    print('arguments:', args)

    cookie = parse_cookie_text(args.cookie_text)
    try:
        episode_num, manga_detail = get_manga_detail(args.manga_id, cookie)
    except Exception as e:
        print('Exception:', e)
        print('Please check your proxy configuration or internet connection.')
        exit(0)
    print(manga_detail['title'], manga_detail['author_name'])
    print(manga_detail['classic_lines'])
    print('episode num:', len(manga_detail['ep_list']))

    episode_list, comic_title = manga_detail["ep_list"], manga_detail["title"]
    for episode in episode_list:
        if episode['title'].strip() == "":
            episode['title'] == episode['short_title']
        if episode["is_locked"]:
            print(
                '{} - {} is locked.'.format(episode['short_title'], episode['title']))
            continue

        save_folder = os.path.join(args.base_folder, comic_title,
                                   '{}-{}'.format(episode['short_title'], episode['title']))
        folder = os.path.exists(save_folder)
        if not folder:
            os.makedirs(save_folder)
        try:
            length, images_list = get_images_list(episode['id'], cookie)
        except Exception as e:
            print('Exception:', e)
            print('Please check your proxy configuration or internet connection.')
            continue

        for i, image in enumerate(tqdm(images_list)):
            try:
                res = download_episode_image(save_folder, image['path'], i)
            except Exception as e:
                print('Exception:', e)
                print('Please check your proxy configuration or internet connection.')
                continue
            if res:
                sleep(args.interval_seconds)  # control speed

    print('finished.')
