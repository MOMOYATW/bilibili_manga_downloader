import AsyncLock from "async-lock";
import {
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import { DownloadItemsRegiter, TaskItem } from "./types";

export class ItemManager {
  register: DownloadItemsRegiter;
  pending: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  downloading: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  complete: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  max_downloading_num: number;
  ipcMain: Electron.IpcMain;
  mainWindow: Electron.CrossProcessExports.BrowserWindow;
  asyncLock: AsyncLock;

  constructor(
    pending: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[],
    complete: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[],
    max_downloading_num: number,
    ipcMain: Electron.IpcMain,
    mainWindow: Electron.CrossProcessExports.BrowserWindow
  ) {
    this.pending = pending;
    this.downloading = [];
    this.complete = complete;
    this.register = {};
    this.max_downloading_num = max_downloading_num;
    this.mainWindow = mainWindow;

    this.asyncLock = new AsyncLock();

    // register for everyone
    pending.map((pendingItem) => {
      this.registerTask(pendingItem);
    });
    complete.map((completeItem) => {
      this.registerTask(completeItem);
    });
    console.log("execute");
    // bind signal
    // querys
    ipcMain.on("getPendingList", () => {
      this.sendPending();
    });
    ipcMain.on("getDownloadingList", () => {
      this.sendDownloading();
    });
    ipcMain.on("getCompleteList", () => {
      this.sendComplete();
    });
    ipcMain.on("getDownloadList", (_event, comicId: number) => {
      this.sendRegister(comicId);
    });
    // operations
    ipcMain.on("deleteComicPending", (_event, comicId: number) => {
      this.pending = this.pending.filter((pendingItem) => {
        if (pendingItem.comic.id === comicId) {
          delete this.register[pendingItem.comic.id][pendingItem.episode.id];
          return false;
        }
        return true;
      });
      this.sendPending();
    });
    ipcMain.on("deleteEpisodePending", (_event, episodeId: number) => {
      this.pending = this.pending.filter((pendingItem) => {
        if (pendingItem.episode.id === episodeId) {
          delete this.register[pendingItem.comic.id][pendingItem.episode.id];
          return false;
        }
        return true;
      });
      this.sendPending();
    });
    ipcMain.on("cancelComicDownloading", (_event, comicId: number) => {
      this.downloading = this.downloading.filter((downloadingItem) => {
        if (downloadingItem.comic.id === comicId) {
          downloadingItem.item.forEach((item) => item.cancel());
          delete this.register[downloadingItem.comic.id][
            downloadingItem.episode.id
          ];
          return false;
        }
        return true;
      });
      this.sendDownloading();
      this.DownloadLoader();
    });
    ipcMain.on("cancelEpisodeDownloading", (_event, episodeId: number) => {
      this.downloading = this.downloading.filter((downloadingItem) => {
        if (downloadingItem.episode.id === episodeId) {
          downloadingItem.item.forEach((item) => item.cancel());
          delete this.register[downloadingItem.comic.id][
            downloadingItem.episode.id
          ];
          return false;
        }
        return true;
      });
      this.sendDownloading();
      this.DownloadLoader();
    });
    ipcMain.on("deleteComicComplete", (_event, comicId: number) => {
      this.complete = this.complete.filter((completeItem, index) => {
        if (completeItem.comic.id === comicId) {
          delete this.register[completeItem.comic.id][completeItem.episode.id];
          return false;
        }
        return true;
      });
      this.sendComplete();
    });
    ipcMain.on("deleteEpisodeComplete", (_event, episodeId: number) => {
      this.complete = this.complete.filter((completeItem, index) => {
        if (completeItem.episode.id === episodeId) {
          delete this.register[completeItem.comic.id][completeItem.episode.id];
          return false;
        }
        return true;
      });
      this.sendComplete();
    });

    this.DownloadLoader();
  }

  public getDownloading() {
    return this.downloading;
  }

  public getComplete() {
    return this.complete;
  }

  public addPending(task: TaskItem<ComicEpisodeObject | ComicPlusItemObject>) {
    this.registerTask(task);
    this.sendRegister(task.comic.id);
    this.pending.push(task);
    this.sendPending();
    this.DownloadLoader();
  }

  public DownloadLoader() {
    // judge if load
    this.asyncLock.acquire("mutex", () => {
      if (
        this.max_downloading_num &&
        this.downloading.length >= this.max_downloading_num
      )
        return;
      // load
      const loadItems = this.pending.splice(
        0,
        this.max_downloading_num - this.downloading.length
      );
      this.sendPending();
      // add to download list
      this.downloading.push(...loadItems);
      this.sendDownloading();
      loadItems.map((item) => {
        item.imageUrls.map((url) =>
          this.mainWindow.webContents.downloadURL(url)
        );
      });
    });
  }

  public downloadComplete(
    task: TaskItem<ComicEpisodeObject | ComicPlusItemObject>
  ) {
    const index = this.downloading.indexOf(task);
    if (index === -1) {
      console.error(
        `complete task doesn't exist in downloading list. ${task.episode.id}`
      );
      return;
    }
    task.item = [];
    this.downloading.splice(index, 1);
    this.complete.push(task);
    this.DownloadLoader();
    this.sendComplete();
    this.sendDownloading();
  }

  public registerTask(
    task: TaskItem<ComicEpisodeObject | ComicPlusItemObject>
  ) {
    if (!this.register[task.comic.id]) {
      this.register[task.comic.id] = {};
    }
    this.register[task.comic.id][task.episode.id] = true;
  }

  public sendPending() {
    this.mainWindow.webContents.send("PendingList", this.pending);
  }

  public sendDownloading() {
    this.mainWindow.webContents.send(
      "DownloadingList",
      this.downloading.map((downloadItem) => ({
        ...downloadItem,
        item: [],
      }))
    );
  }

  public sendComplete() {
    this.mainWindow.webContents.send("CompleteList", this.complete);
  }

  public sendRegister(comicId: number) {
    this.mainWindow.webContents.send(
      "DownloadList",
      this.register[comicId] ? this.register[comicId] : {}
    );
  }

  public updateMaxDownloadingNum(updateNumber: number) {
    this.max_downloading_num = updateNumber;
    this.DownloadLoader();
  }
}
