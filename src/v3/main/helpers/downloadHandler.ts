import path from "path";
import os from "os";
import fs from "fs";
import { ItemManager } from "../dlItemManager";
import { MappingManager } from "../dlItemsMappingManager";
import { generateComicPath, generateEpisodePath, generateImageName, generateMetadata, generateTokutenPath, readJSONasObject, slugify } from "../utils";
import { app_folder, config } from "./configHandler";
import { ComicDetailData, ComicEpisodeObject, ComicPlusItemObject } from "../bilibili-manga-client";
import { api } from "./apiHandler";
import { DownloadPlusInfo, TaskItem } from "../types";

export const mappingManager = new MappingManager();
export const itemManager = new ItemManager(
    readJSONasObject(path.join(os.homedir(), app_folder, "complete.json"), []),
    config.get('max_download_num'),
    config.get('zip_options'));

export function handleWillDownload(_event: Electron.IpcMainEvent, item: Electron.DownloadItem, _webContents: any) {
    const serverSideName = item.getFilename();

    if (!mappingManager.recordExist(serverSideName)) {
        console.error(`Item canceled due to lack of task information. serverSideName: ${serverSideName}`);
        item.cancel();
        return;
    }

    const mappingInfo = mappingManager.getMappingInfo(serverSideName, itemManager.getDownloading());

    if (mappingInfo.episodeId === null) {
        item.setSavePath(path.join(config.get('download_path'), mappingInfo.filename));
        return;
    }

    const downloadItem = itemManager.getDownloading().find(downloadingItem => downloadingItem.episode.id === mappingInfo.episodeId);

    if (!downloadItem) {
        console.error(`item cannot find its download info. episodeId: ${mappingInfo.episodeId} filename: ${mappingInfo.filename}`);
        item.cancel();
        return;
    }

    const savePath = path.join(config.get('download_path'), mappingInfo.filename);

    if (fs.existsSync(savePath)) {
        item.cancel();
        downloadItem.finished_num += 1;
        if (downloadItem.finished_num === downloadItem.task_num) {
            itemManager.downloadComplete(downloadItem);
        }
        console.log("Already downloaded. Download canceled.");
        return;
    }

    item.setSavePath(savePath);
    downloadItem.item.push(item);

    let lastReceivedBytes = 0;

    item.on("updated", (_event, state) => {
        if (state === "interrupted") {
            console.log("Download is interrupted but can be resumed");
            console.log(downloadItem.savePath);
        } else if (state === "progressing") {
            if (item.isPaused()) {
                console.log("Download is paused");
            } else {
                const deltaItemProgress = (item.getReceivedBytes() - lastReceivedBytes) / item.getTotalBytes();
                downloadItem.progress += (deltaItemProgress / downloadItem.task_num) * 100;
                lastReceivedBytes = item.getReceivedBytes();
                itemManager.sendDownloading();
            }
        }
    });

    item.once("done", (_event, state) => {
        if (state === "completed") {
            downloadItem.finished_num += 1;
            if (downloadItem.finished_num === downloadItem.task_num) {
                itemManager.downloadComplete(downloadItem);
            }
            console.log("Download successfully");
        } else {
            console.log(`Download failed: ${state}`);
        }
    });
}

export async function handleDownloadEpisodes(event: Electron.IpcMainEvent, comicInfo: ComicDetailData) {
    if (comicInfo.ep_list.length === 0) return;
    // download cover issue #7
    const serverSideName =
        comicInfo.vertical_cover.split("/")[
        comicInfo.vertical_cover.split("/").length - 1
        ];
    const comicFolderName = generateComicPath(
        config.get('comic_folder_format'),
        comicInfo
    );
    const imageName = "cover";
    const clientSideName = path.join(
        slugify(comicFolderName),
        slugify(imageName) +
        "." +
        serverSideName.split(".")[serverSideName.split(".").length - 1]
    );
    mappingManager.registerMappingInfo(serverSideName, {
        episodeId: null,
        filename: clientSideName,
    });
    event.sender.downloadURL(comicInfo.vertical_cover);
    // save metadata
    if (config.get('save_meta_data')) {
        generateMetadata(
            config.get('meta_data_options'),
            comicInfo,
            config.get('download_path'),
            config.get('comic_folder_format')
        );
    }

    // handle selected list
    // currently type can only be video or images

    Promise.allSettled(
        comicInfo.ep_list.map(async (episode) => {
            let video_task = false;
            const imageIndexs = await api.getImageIndex(episode.id);
            const imageHost = imageIndexs.data.data.host;
            const imageUrls = imageIndexs.data.data.images.map(
                (image, imageIndex) => {
                    let serverSideName = "";
                    // judge if image or video
                    if (image.video_path) {
                        // use video_path
                        video_task = true;
                        serverSideName = image.video_path
                            .split("/")
                        [image.video_path.split("/").length - 1].split("?")[0];
                    } else {
                        serverSideName =
                            image.path.split("/")[image.path.split("/").length - 1];
                    }
                    const comicFolderName = generateComicPath(
                        config.get('comic_folder_format'),
                        comicInfo
                    );
                    const episodeFolderName = generateEpisodePath(
                        config.get('episode_folder_format'),
                        episode
                    );
                    const imageName = generateImageName(
                        config.get('image_file_format'),
                        imageIndex
                    );
                    const clientSideName = path.join(
                        slugify(comicFolderName),
                        config.get('seperate_folder') ? "正篇" : "",
                        slugify(episodeFolderName),
                        slugify(imageName) +
                        "." +
                        serverSideName.split(".")[serverSideName.split(".").length - 1]
                    );
                    mappingManager.registerMappingInfo(serverSideName, {
                        episodeId: episode.id,
                        filename: clientSideName,
                    });
                    if (video_task) {
                        // if video
                        return image.video_path;
                    } else {
                        return imageHost + image.path;
                    }
                }
            );
            let imageUrlswithToken = [];
            if (video_task) {
                imageUrlswithToken = imageUrls;
            } else {
                const imageTokens = await api.getImageToken(imageUrls);
                imageUrlswithToken = imageTokens.data.data.map((imageToken) => {
                    return imageToken.url + "?token=" + imageToken.token;
                });
            }
            const comicFolderName = generateComicPath(
                config.get('comic_folder_format'),
                comicInfo
            );
            const episodeFolderName = generateEpisodePath(
                config.get('episode_folder_format'),
                episode
            );
            const episodeWithUrls: TaskItem<
                ComicEpisodeObject | ComicPlusItemObject
            > = {
                episode,
                imageUrls: imageUrlswithToken,
                comic: {
                    id: comicInfo.id,
                    title: comicInfo.title,
                    cover: comicInfo.horizontal_cover,
                },
                progress: 0,
                finished_num: 0,
                task_num: imageUrlswithToken.length,
                item: [],
                type: "episode",
                savePath: path.join(
                    config.get('download_path'),
                    slugify(comicFolderName),
                    config.get('seperate_folder') ? "正篇" : "",
                    slugify(episodeFolderName)
                ),
            };
            itemManager.addPending(episodeWithUrls);
        })
    );
}

export async function handleDownloadPlusEpisodes(event: Electron.IpcMainEvent, comicInfo: DownloadPlusInfo) {
    if (comicInfo.ep_list.length === 0) return;
    // handle selected list
    // check type
    Promise.allSettled(
        comicInfo.ep_list.map(async (episode) => {
            let urlsInfo: string[];
            if (!episode.item.pic_num) {
                // video type
                urlsInfo = [episode.item.video.url];
            } else {
                urlsInfo = episode.item.pic;
            }
            const imageUrls = urlsInfo.map((image, imageIndex) => {
                const serverSideName = image.split("?")[0].split("/")[
                    image.split("/").length - 1
                ];
                const comicFolderName = generateComicPath(
                    config.get('comic_folder_format'),
                    comicInfo.comic
                );
                const episodeFolderName = generateTokutenPath(
                    config.get('tokuten_folder_format'),
                    episode.item
                );
                const imageName = generateImageName(
                    config.get('image_file_format'),
                    imageIndex
                );
                const clientSideName = path.join(
                    slugify(comicFolderName),
                    config.get('seperate_folder') ? "特典" : "",
                    slugify(episodeFolderName),
                    slugify(imageName) +
                    "." +
                    serverSideName.split(".")[serverSideName.split(".").length - 1]
                );
                mappingManager.registerMappingInfo(serverSideName, {
                    episodeId: episode.item.id,
                    filename: clientSideName,
                });
                return image;
            });
            // # issue 27 add token check
            let imageUrlswithToken = [];
            if (!episode.item.pic_num) {
                imageUrlswithToken = imageUrls;
            } else {
                const imageTokens = await api.getImageToken(imageUrls);
                imageUrlswithToken = imageTokens.data.data.map((imageToken) => {
                    return imageToken.url + "?token=" + imageToken.token;
                });
            }

            const comicFolderName = generateComicPath(
                config.get('comic_folder_format'),
                comicInfo.comic
            );
            const episodeFolderName = generateTokutenPath(
                config.get('tokuten_folder_format'),
                episode.item
            );
            const episodeWithUrls: TaskItem<
                ComicEpisodeObject | ComicPlusItemObject
            > = {
                episode: episode.item,
                imageUrls: imageUrlswithToken,
                comic: {
                    id: comicInfo.comic.id,
                    title: comicInfo.comic.title,
                    cover: comicInfo.comic.horizontal_cover,
                },
                progress: 0,
                finished_num: 0,
                task_num: imageUrlswithToken.length,
                item: [],
                type: !episode.item.pic_num ? "tokuten-video" : "tokuten-image",
                savePath: path.join(
                    config.get('download_path'),
                    slugify(comicFolderName),
                    config.get('seperate_folder') ? "特典" : "",
                    slugify(episodeFolderName)
                ),
            };
            itemManager.addPending(episodeWithUrls);
        })
    );
}

export function saveRecord() {
    fs.writeFileSync(
        path.join(os.homedir(), app_folder, "complete.json"),
        JSON.stringify(itemManager.getComplete())
    );
}