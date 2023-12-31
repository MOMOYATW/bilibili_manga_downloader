import os from "os";
import path from "path";
import { app, BrowserWindow, dialog, ipcMain, session } from "electron";
import serve from "electron-serve";
import { createWindow } from "./helpers";
import { autoUpdater } from "electron-updater";
import {
  BilibiliMangaAPI,
  ComicDetailData,
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import {
  slugify,
  writeObjectasJSON,
  zipDirectory,
  generateComicPath,
  generateEpisodePath,
  generateImageName,
  generateTokutenPath,
  generateMetadata,
} from "./utils";
import { bindWindowBtns } from "./bindWindowBtns";
import { DownloadPlusInfo, TaskItem } from "./types";
import { createTray } from "./createTray";
import { config, app_folder } from "./helpers/configHandler";
import { handleWillDownload } from "./helpers/downloadHandler";
import { itemManager, mappingManager } from "./helpers/downloadHandler";

const isProd: boolean = process.env.NODE_ENV === "production";

if (!app.requestSingleInstanceLock()) {
  app.quit();
}

if (isProd) {
  serve({ directory: "app" });
} else {
  app.setPath("userData", `${app.getPath("userData")} (development)`);
}

const api = new BilibiliMangaAPI({ authToken: config.get('token') });

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

  app.on("second-instance", () => {
    mainWindow.show();
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  });

  // set up a tray
  createTray(mainWindow, () => {
    writeObjectasJSON(
      path.join(os.homedir(), app_folder, "config.json"),
      config.getConfig()
    );
    writeObjectasJSON(
      path.join(os.homedir(), app_folder, "complete.json"),
      itemManager.getComplete()
    );
  });

  ipcMain.on("getVersion", () => {
    mainWindow.webContents.send("Version", app.getVersion());
  });

  if (process.platform === "win32") {
    app.setAppUserModelId(app.name);
  }

  autoUpdater.checkForUpdatesAndNotify();

  if (isProd) {
    await mainWindow.loadURL("app://./home.html");
  } else {
    const port = process.argv[2];
    await mainWindow.loadURL(`http://localhost:${port}/home`);
    mainWindow.webContents.openDevTools();
  }


  itemManager.on("PendingList", (pendingList) => mainWindow.webContents.send("PendingList", pendingList));
  itemManager.on("DownloadingList", (downloadingList) => mainWindow.webContents.send("DownloadingList", downloadingList));
  itemManager.on("CompleteList", (completeList) => mainWindow.webContents.send("CompleteList", completeList));
  itemManager.on("Register", (comicId) => mainWindow.webContents.send("Register", comicId));
  itemManager.on("downloadItem", (url) => mainWindow.webContents.downloadURL(url));

  ipcMain.on("getPendingList", () => itemManager.sendPending());
  ipcMain.on("getDownloadingList", () => itemManager.sendDownloading());
  ipcMain.on("getCompleteList", () => itemManager.sendComplete());
  ipcMain.on("getDownloadList", (_event, comicId: number) => itemManager.sendRegister(comicId));
  ipcMain.on("deleteComicPending", (_event, comicId: number) => itemManager.removePendingByComicId(comicId));
  ipcMain.on("deleteEpisodePending", (_event, episodeId: number) => itemManager.removePendingByEpisodeId(episodeId));
  ipcMain.on("cancelComicDownloading", (_event, comicId: number) => itemManager.removeDownloadingByComicId(comicId));
  ipcMain.on("cancelEpisodeDownloading", (_event, episodeId: number) => itemManager.removeDownloadingByEpisodeId(episodeId));
  ipcMain.on("deleteComicComplete", (_event, comicId: number) => itemManager.removeCompleteByComicId(comicId));
  ipcMain.on("deleteEpisodeComplete", (_event, episodeId: number) => itemManager.removeCompleteByEpisodeId(episodeId));

  mainWindow.webContents.session.on("will-download", handleWillDownload);

  ipcMain.on("getSearch", async (event, args: string) => {
    try {
      const result = await api.getSearch(args);
      mainWindow.webContents.send("Search", result.data.data.list);
    } catch (error) {
      console.log(error);
      mainWindow.webContents.send("Search", []);
    }
  });

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
    zipDirectory(args, args + ".7z", () => { });
  });

  ipcMain.on("getCurrentConfig", () => {
    mainWindow.webContents.send("CurrentConfig", config.getConfig());
  });

  ipcMain.on("updateConfig", (event, args) => {
    config.update(args);
    api.updateConfig({ authToken: config.get('token') });
    itemManager.updateConfig({ max_downloading_num: config.get('max_download_num'), zip_options: config.get('zip_options') });
  });

  ipcMain.on("openDialog", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
      properties: ["openDirectory"],
    });
    if (canceled) return;
    config.update({ download_path: filePaths[0] })
    mainWindow.webContents.send("CurrentConfig", config.getConfig());
  });

  ipcMain.on("DownloadEpisodes", async (event, comicInfo: ComicDetailData) => {
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
    mainWindow.webContents.downloadURL(comicInfo.vertical_cover);
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
  );

  bindWindowBtns(ipcMain, mainWindow);

  //Close the app
  ipcMain.on("closeApp", () => {
    if (config.get('hide_in_tray')) mainWindow.hide();
    else {
      writeObjectasJSON(
        path.join(os.homedir(), app_folder, "config.json"),
        config.getConfig()
      );
      writeObjectasJSON(
        path.join(os.homedir(), app_folder, "complete.json"),
        itemManager.getComplete()
      );
      mainWindow.close();
    }
  });

  ipcMain.on("saveMetadata", (event, comicInfo: ComicDetailData) => {
    generateMetadata(
      config.get('meta_data_options'),
      comicInfo,
      config.get('download_path'),
      config.get('comic_folder_format')
    );
  });

  ipcMain.on("openBilibiliManga", () => {
    const win = new BrowserWindow({
      width: 800,
      height: 600,
    });
    win.loadURL("https://manga.bilibili.com");
    win.setMenu(null);
    win.webContents.on("did-frame-finish-load", () => {
      win.setTitle("登陆完成后关闭窗口即可");
    });
    const ses = win.webContents.session.cookies;
    win.on("close", () => {
      ses
        .get({ url: "https://manga.bilibili.com/" })
        .then((cookies) => {
          const sessdata = cookies.filter((map) => map.name === "SESSDATA")[0];
          if (sessdata === undefined) return;
          config.update({ token: sessdata.value });
          mainWindow.webContents.send("CurrentConfig");
        })
        .catch((error) => {
          console.log(error);
        });
    });
  });
})();

app.on("window-all-closed", () => {
  app.quit();
});
