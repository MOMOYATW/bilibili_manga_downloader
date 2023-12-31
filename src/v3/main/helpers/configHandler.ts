import path from "path";
import os from "os";
import { ConfigManager } from "../configManager";
import { readJSONasObject } from "../utils";
export const app_folder = ".bilibili_manga_downloader";
export const config = new ConfigManager(readJSONasObject(path.join(os.homedir(), app_folder, "config.json"), {}));