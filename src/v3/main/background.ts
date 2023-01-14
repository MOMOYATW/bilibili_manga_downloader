import os from "os";
import path from "path";
import serve from "electron-serve";
import { app, dialog, ipcMain, session } from "electron";
import { createWindow } from "./helpers";
import {
  BilibiliMangaAPI,
  ComicDetailData,
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import { Config, DownloadPlusInfo, TaskItem } from "./types";
import {
  readJSONasObjectUpdate,
  readJSONasObject,
  slugify,
  writeObjectasJSON,
  zipDirectory,
  generateComicPath,
  generateEpisodePath,
  generateImageName,
  generateTokutenPath,
} from "./utils";
import { bindWindowBtns } from "./bindWindowBtns";
import { MappingManager } from "./dlItemsMappingManager";
import { ItemManager } from "./dlItemManager";

const isProd: boolean = process.env.NODE_ENV === "production";

if (isProd) {
  serve({ directory: "app" });
} else {
  app.setPath("userData", `${app.getPath("userData")} (development)`);
}

let config: Config = {
  token: "",
  download_path: path.join(os.homedir(), "download_comics"),
  comic_folder_format: "{title}",
  episode_folder_format: "{index}-{title}",
  tokuten_folder_format: "{title}",
  image_file_format: "{index}",
  max_download_num: 1,
  zip_after_download: false,
};

const app_folder = ".bilibili_manga_downloader";
config = readJSONasObjectUpdate<Config>(
  path.join(os.homedir(), app_folder, "config.json"),
  config
);

const api = new BilibiliMangaAPI({ authToken: config.token });

const mappingManager = new MappingManager();

(async () => {
  await app.whenReady();

  session.defaultSession.webRequest.onBeforeSendHeaders(
    { urls: ["https://*.bilivideo.com/*"] },
    (details, callback) => {
      (details.requestHeaders["User-Agent"] = "Bilibili"),
        callback({ requestHeaders: details.requestHeaders });
    }
  );

  const mainWindow = createWindow("main", {
    width: 1000,
    height: 600,
  });

  if (isProd) {
    await mainWindow.loadURL("app://./home.html");
  } else {
    const port = process.argv[2];
    await mainWindow.loadURL(`http://localhost:${port}/home`);
    mainWindow.webContents.openDevTools();
  }

  const itemManager = new ItemManager(
    [],
    readJSONasObject(path.join(os.homedir(), app_folder, "complete.json"), []),
    config.max_download_num,
    ipcMain,
    mainWindow
  );

  mainWindow.webContents.session.on(
    "will-download",
    (event, item, webContents) => {
      const serverSideName = item.getFilename();

      if (!mappingManager.recordExist(serverSideName)) {
        // cannot find record, handle it nicely.
        console.error(
          `Item canceled due to lack of task information. serverSideName: ${serverSideName}`
        );
        item.cancel();
        return;
      }

      const mappingInfo = mappingManager.getMappingInfo(
        serverSideName,
        itemManager.getDownloading()
      );

      // check if is cover
      if (mappingInfo.episodeId === null) {
        item.setSavePath(path.join(config.download_path, mappingInfo.filename));
        return;
      }

      // get downloading item info
      const downloadItem = itemManager
        .getDownloading()
        .filter((downloadingItem) => {
          return downloadingItem.episode.id === mappingInfo.episodeId;
        })[0];

      if (!downloadItem) {
        // cannot fimd downloading item info, handle it nicely
        console.error(
          `item cannot find its download info. episodeId: ${mappingInfo.episodeId} filename: ${mappingInfo.filename}`
        );
        item.cancel();
        return;
      }

      // set download path
      item.setSavePath(path.join(config.download_path, mappingInfo.filename));
      downloadItem.item.push(item);

      // global variable
      let lastReceivedBytes = 0;

      // update
      item.on("updated", (event, state) => {
        if (state == "interrupted") {
          console.log("Download is interrupted but can be resume");
        } else if (state == "progressing") {
          if (item.isPaused()) {
            console.log("Download is paused");
          } else {
            const deltaItemProgress =
              (item.getReceivedBytes() - lastReceivedBytes) /
              item.getTotalBytes();
            downloadItem.progress +=
              (deltaItemProgress / downloadItem.task_num) * 100;
            lastReceivedBytes = item.getReceivedBytes();
            itemManager.sendDownloading();
          }
        }
      });

      // done
      item.once("done", (event, state) => {
        if (state === "completed") {
          downloadItem.finished_num += 1;
          if (downloadItem.finished_num === downloadItem.task_num) {
            // archive to file
            const episode_folder = path.join(
              ...item.savePath
                .split(path.sep)
                .splice(0, item.savePath.split(path.sep).length - 1)
            );
            const comic_folder = path.join(
              ...episode_folder
                .split(path.sep)
                .splice(0, episode_folder.split(path.sep).length - 1)
            );
            if (config.zip_after_download) {
              zipDirectory(comic_folder, comic_folder + ".zip", () => {});
            }
            itemManager.downloadComplete(downloadItem);
          }
          console.log("Download successfully");
        } else {
          console.log(`Download failed: ${state}`);
        }
      });
    }
  );

  ipcMain.on("getComicDetail", async (event, args: number) => {
    try {
      const result = await api.getComicDetail(args);
      mainWindow.webContents.send("ComicDetail", result.data.data);
    } catch (error) {
      console.log(error);
      mainWindow.webContents.send("ComicDetail", null);
    }
  });

  ipcMain.on("getComicAlbumPlus", async (event, args: number) => {
    try {
      const result = await api.getComicAlbumPlus(args);
      mainWindow.webContents.send("ComicAlbumPlus", result.data.data);
    } catch (error) {
      console.log(error);
      mainWindow.webContents.send("ComicAlbumPlus", null);
    }
  });

  ipcMain.on("zipFolder", (event, args) => {
    zipDirectory(args, args + ".zip", () => {});
  });

  ipcMain.on("getCurrentConfig", () => {
    mainWindow.webContents.send("CurrentConfig", config);
  });

  ipcMain.on("updateConfig", (event, args) => {
    config = args;
    api.updateConfig({ authToken: config.token });
    itemManager.updateMaxDownloadingNum(config.max_download_num);
  });

  ipcMain.on("openDialog", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
      properties: ["openDirectory"],
    });
    if (canceled) return;
    config.download_path = filePaths[0];
    mainWindow.webContents.send("CurrentConfig", config);
  });

  ipcMain.on("DownloadEpisodes", async (event, comicInfo: ComicDetailData) => {
    if (comicInfo.ep_list.length === 0) return;
    // download cover issue #7
    const serverSideName =
      comicInfo.vertical_cover.split("/")[
        comicInfo.vertical_cover.split("/").length - 1
      ];
    const comicFolderName = generateComicPath(
      config.comic_folder_format,
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
    mainWindow.webContents.downloadURL(comicInfo.vertical_cover);
    // handle selected list
    Promise.allSettled(
      comicInfo.ep_list.map(async (episode) => {
        const imageIndexs = await api.getImageIndex(episode.id);
        const imageHost = imageIndexs.data.data.host;
        const imageUrls = imageIndexs.data.data.images.map(
          (image, imageIndex) => {
            const serverSideName =
              image.path.split("/")[image.path.split("/").length - 1];
            const comicFolderName = generateComicPath(
              config.comic_folder_format,
              comicInfo
            );
            const episodeFolderName = generateEpisodePath(
              config.episode_folder_format,
              episode
            );
            const imageName = generateImageName(
              config.image_file_format,
              imageIndex
            );
            const clientSideName = path.join(
              slugify(comicFolderName),
              slugify(episodeFolderName),
              slugify(imageName) +
                "." +
                serverSideName.split(".")[serverSideName.split(".").length - 1]
            );
            mappingManager.registerMappingInfo(serverSideName, {
              episodeId: episode.id,
              filename: clientSideName,
            });
            return imageHost + image.path;
          }
        );
        const imageTokens = await api.getImageToken(imageUrls);
        const imageUrlswithToken = imageTokens.data.data.map((imageToken) => {
          return imageToken.url + "?token=" + imageToken.token;
        });
        const comicFolderName = generateComicPath(
          config.comic_folder_format,
          comicInfo
        );
        const episodeFolderName = generateEpisodePath(
          config.episode_folder_format,
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
            config.download_path,
            comicFolderName,
            episodeFolderName
          ),
        };
        itemManager.addPending(episodeWithUrls);
      })
    );
  });

  ipcMain.on(
    "DownloadPlusEpisodes",
    async (event, comicInfo: DownloadPlusInfo) => {
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
              config.comic_folder_format,
              comicInfo.comic
            );
            const episodeFolderName = generateTokutenPath(
              config.tokuten_folder_format,
              episode.item
            );
            const imageName = generateImageName(
              config.image_file_format,
              imageIndex
            );
            const clientSideName = path.join(
              slugify(comicFolderName),
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
          const comicFolderName = generateComicPath(
            config.comic_folder_format,
            comicInfo.comic
          );
          const episodeFolderName = generateTokutenPath(
            config.tokuten_folder_format,
            episode.item
          );
          const episodeWithUrls: TaskItem<
            ComicEpisodeObject | ComicPlusItemObject
          > = {
            episode: episode.item,
            imageUrls,
            comic: {
              id: comicInfo.comic.id,
              title: comicInfo.comic.title,
              cover: comicInfo.comic.horizontal_cover,
            },
            progress: 0,
            finished_num: 0,
            task_num: imageUrls.length,
            item: [],
            type: !episode.item.pic_num ? "tokuten-video" : "tokuten-image",
            savePath: path.join(
              config.download_path,
              comicFolderName,
              episodeFolderName
            ),
          };
          itemManager.addPending(episodeWithUrls);
        })
      );
    }
  );

  bindWindowBtns(ipcMain, mainWindow, () => {
    writeObjectasJSON(
      path.join(os.homedir(), app_folder, "config.json"),
      config,
      path.join(os.homedir(), app_folder)
    );
    writeObjectasJSON(
      path.join(os.homedir(), app_folder, "complete.json"),
      itemManager.getComplete(),
      path.join(os.homedir(), app_folder)
    );
  });
})();

app.on("window-all-closed", () => {
  app.quit();
});

ipcMain.on("ping-pong", (event, arg) => {
  // event.sender.send("ping-pong", `[ipcMain] "${arg}" received asynchronously.`);
  console.log(arg);
});