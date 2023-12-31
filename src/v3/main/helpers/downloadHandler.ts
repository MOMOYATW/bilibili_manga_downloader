import path from "path";
import os from "os";
import fs from "fs";
import { ItemManager } from "../dlItemManager";
import { MappingManager } from "../dlItemsMappingManager";
import { readJSONasObject } from "../utils";
import { app_folder, config } from "./configHandler";

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