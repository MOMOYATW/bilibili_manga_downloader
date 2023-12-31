import { app, BrowserWindow, ipcMain, session } from "electron";
import serve from "electron-serve";
import { autoUpdater } from "electron-updater";
import { createWindow } from "./helpers";
import { config, handleOpenConfigDialog, saveConfig } from "./helpers/configHandler";
import { api, handleGetComicAlbumPlus, handleGetComicDetail, handleGetSearch } from "./helpers/apiHandler";
import { itemManager, handleDownloadEpisodes, handleDownloadPlusEpisodes, handleWillDownload, saveRecord } from "./helpers/downloadHandler";
import { ComicDetailData, } from "./bilibili-manga-client";
import { zipDirectory, generateMetadata, } from "./utils";
import { createTray } from "./createTray";

const isProd: boolean = process.env.NODE_ENV === "production";

if (!app.requestSingleInstanceLock()) {
  app.quit();
}

if (isProd) {
  serve({ directory: "app" });
} else {
  app.setPath("userData", `${app.getPath("userData")} (development)`);
}



(async () => {
  await app.whenReady();

  config.setUpdatedCallback(() => {
    api.updateConfig({ authToken: config.get('token') });
    itemManager.updateConfig({ max_downloading_num: config.get('max_download_num'), zip_options: config.get('zip_options') });
  })

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

  const showWindow = () => {
    mainWindow.show();
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  }

  const closeWindow = () => {
    saveConfig();
    saveRecord();
    mainWindow.close();
  }

  // set up a tray
  createTray(showWindow, closeWindow);

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
  itemManager.on("DownloadList", (comicId) => mainWindow.webContents.send("DownloadList", comicId));
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

  ipcMain.on("getSearch", handleGetSearch);
  ipcMain.on("getComicDetail", handleGetComicDetail);
  ipcMain.on("getComicAlbumPlus", handleGetComicAlbumPlus);

  ipcMain.on("zipFolder", (_event, args) => zipDirectory(args, args + ".7z", () => { }));

  ipcMain.on("getCurrentConfig", () => mainWindow.webContents.send("CurrentConfig", config.getConfig()));
  ipcMain.on("updateConfig", (_event, args) => config.update(args));
  ipcMain.on("openConfigDialog", handleOpenConfigDialog);

  ipcMain.on("DownloadEpisodes", handleDownloadEpisodes);
  ipcMain.on("DownloadPlusEpisodes", handleDownloadPlusEpisodes);

  ipcMain.on("minimiseApp", () => mainWindow.minimize());
  ipcMain.on("maximizeRestoreApp", () => {
    if (mainWindow.isMaximized()) mainWindow.restore() 
    else mainWindow.maximize();
  });
  mainWindow.on("maximize", () => mainWindow.webContents.send("isMaximized"));
  mainWindow.on("unmaximize", () => mainWindow.webContents.send("isRestored"));
  //Close the app
  ipcMain.on("closeApp", () => {
    if (config.get('hide_in_tray')) mainWindow.hide();
    else closeWindow();
  });

  ipcMain.on("saveMetadata", (_event, comicInfo: ComicDetailData) => {
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
          mainWindow.webContents.send("CurrentConfig", config.getConfig());
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
