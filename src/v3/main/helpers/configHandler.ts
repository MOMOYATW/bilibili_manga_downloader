import path from "path";
import os from "os";
import { ConfigManager } from "../configManager";
import { readJSONasObject, writeObjectasJSON } from "../utils";
import { dialog } from "electron";
export const app_folder = ".bilibili_manga_downloader";
export const config = new ConfigManager(readJSONasObject(path.join(os.homedir(), app_folder, "config.json"), {}));

export async function handleOpenConfigDialog(event: Electron.IpcMainEvent) {
    const { canceled, filePaths } = await dialog.showOpenDialog({
        properties: ["openDirectory"],
    });
    if (canceled) return;
    config.update({ download_path: filePaths[0] })
    event.sender.send("CurrentConfig", config.getConfig());
}

export function saveConfig() {
    writeObjectasJSON(
        path.join(os.homedir(), app_folder, "config.json"),
        config.getConfig()
    );
}