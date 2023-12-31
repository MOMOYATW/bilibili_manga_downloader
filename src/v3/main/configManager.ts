// create a ConfigManager class to store the configuration
import os from "os";
import path from "path";
import { Config } from "./types";

const defaultConfig: Config = {
    token: "",
    download_path: path.join(os.homedir(), "download_comics"),
    comic_folder_format: "{title}",
    episode_folder_format: "{index}-{title}",
    tokuten_folder_format: "{title}",
    image_file_format: "{index}",
    max_download_num: 1,
    hide_in_tray: true,
    seperate_folder: false,
    meta_data_options: "tachiyomi",
    save_meta_data: false,
    zip_options: "no_zip",
};


export class ConfigManager {
    private config: Config = defaultConfig;
    private updatedCallback: Function = () => { };
    constructor(config: Partial<Config>, updatedCallback: Function = () => { }) {
        this.update(config);
        this.updatedCallback = updatedCallback;
    }
    public get(key: string) {
        return this.config[key];
    }
    public getConfig() {
        return this.config;
    }
    public setUpdatedCallback(updatedCallback: Function) {
        this.updatedCallback = updatedCallback;
    }
    public update(newConfig: Partial<Config>) {
        for (const key in newConfig) {
            this.config[key] = newConfig[key];
        }
        this.updatedCallback();
    }
}