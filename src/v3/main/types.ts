import { ComicDetailData, ComicPlusObject } from "./bilibili-manga-client";

export interface Config {
  token: string;
  download_path: string;
  comic_folder_format: string;
  episode_folder_format: string;
  tokuten_folder_format: string;
  image_file_format: string;
  max_download_num: number;
  hide_in_tray: boolean;
  seperate_folder: boolean;
  meta_data_options: "tachiyomi";
  save_meta_data: false;
  zip_options: "no_zip" | "zip_comic" | "zip_episode";
}

export interface TaskItem<T> {
  comic: {
    id: number;
    title: string;
    cover: string;
  };
  episode: T;
  progress: number;
  task_num: number;
  finished_num: number;
  item: Electron.DownloadItem[];
  imageUrls: string[];
  type: "episode" | "tokuten-image" | "tokuten-video";
  savePath: string;
}

export interface DownloadItemsMapping {
  [key: string]: {
    episodeId: number;
    filename: string;
  }[];
}

export interface DownloadItemsRegiter {
  [key: string]: {
    [key: string]: boolean;
  };
}

export interface DownloadPlusInfo {
  comic: ComicDetailData;
  ep_list: ComicPlusObject[];
}
