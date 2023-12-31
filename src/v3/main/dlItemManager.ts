import AsyncLock from "async-lock";
import path from "path";
import {
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import { DownloadItemsRegiter, TaskItem } from "./types";
import { zipDirectory } from "./utils";
import EventEmitter from "events";

/**
 * Manages the download items for the manga downloader.
 */
export class ItemManager extends EventEmitter {
  private register: DownloadItemsRegiter;
  private pending: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  private downloading: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  private complete: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
  private asyncLock: AsyncLock;
  private config: {max_downloading_num: number, zip_options: "no_zip" | "zip_comic" | "zip_episode"};

  /**
   * Constructs a new instance of the ItemManager class.
   * @param complete The list of complete download items.
   * @param max_downloading_num The maximum number of items that can be downloaded simultaneously.
   * @param zip_options The options for zipping the downloaded items.
   */
  constructor(
    complete: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[],
    max_downloading_num: number,
    zip_options: "no_zip" | "zip_comic" | "zip_episode"
  ) {
    super();
    this.pending = [];
    this.downloading = [];
    this.complete = complete;
    this.register = {};
    this.config = { max_downloading_num, zip_options };
    this.asyncLock = new AsyncLock();

    // register for everyone
    complete.forEach(item => this.registerTask(item));
    this.DownloadLoader();
  }

  /**
   * Gets the list of currently downloading items.
   * @returns The list of currently downloading items.
   */
  public getDownloading() {
    return this.downloading;
  }

  /**
   * Gets the list of complete download items.
   * @returns The list of complete download items.
   */
  public getComplete() {
    this.complete = this.complete.map((completeItem) => {
      completeItem.imageUrls = [];
      return completeItem;
    });
    return this.complete;
  }

  /**
   * Adds a pending download task.
   * @param task The download task to add.
   */
  public addPending(task: TaskItem<ComicEpisodeObject | ComicPlusItemObject>) {
    this.registerTask(task);
    this.sendRegister(task.comic.id);
    this.pending.push(task);
    this.sendPending();
    this.DownloadLoader();
  }

  public removePendingByComicId(comicId: number) {
    // remove from pending and register
    this.pending = this.pending.filter((item) => item.comic.id !== comicId);
    delete this.register[comicId];
    this.sendPending();
  }

  public removePendingByEpisodeId(episodeId: number) {
    // remove from pending and register
    this.pending = this.pending.filter((item) => item.episode.id !== episodeId);
    Object.keys(this.register).forEach((comicId) => {
      delete this.register[comicId][episodeId];
    });
    this.sendPending();
  }

  public removeDownloadingByComicId(comicId: number) {
    // remove from downloading and register
    this.downloading = this.downloading.filter((item) => item.comic.id !== comicId);
    delete this.register[comicId];
    this.sendDownloading();
    this.DownloadLoader();
  }

  public removeDownloadingByEpisodeId(episodeId: number) {
    // remove from downloading and register
    this.downloading = this.downloading.filter((item) => item.episode.id !== episodeId);
    Object.keys(this.register).forEach((comicId) => {
      delete this.register[comicId][episodeId];
    });
    this.sendDownloading();
    this.DownloadLoader();
  }

  public removeCompleteByComicId(comicId: number) {
    // remove from complete and register
    this.complete = this.complete.filter((item) => item.comic.id !== comicId);
    delete this.register[comicId];
    this.sendComplete();
  }

  public removeCompleteByEpisodeId(episodeId: number) {
    // remove from complete and register
    this.complete = this.complete.filter((item) => item.episode.id !== episodeId);
    Object.keys(this.register).forEach((comicId) => {
      delete this.register[comicId][episodeId];
    });
    this.sendComplete();
  }

  /**
   * Loads and starts downloading the pending items.
   */
  private DownloadLoader() {
    // judge if load
    this.asyncLock.acquire("mutex", () => {
      if (
        this.config.max_downloading_num &&
        this.downloading.length >= this.config.max_downloading_num
      )
        return;
      // load
      const loadItems = this.pending.splice(
        0,
        this.config.max_downloading_num - this.downloading.length
      );
      this.sendPending();
      // add to download list
      this.downloading.push(...loadItems);
      this.sendDownloading();
      loadItems.map((item) => {
        item.imageUrls.map((url) =>
          this.emit("downloadItem", url)
        );
      });
    });
  }

  /**
   * Handles the completion of a download task.
   * @param task The completed download task.
   */
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
    task.imageUrls = [];
    // zip this comic if this the last episode
    if (
      this.config.zip_options === "zip_comic" &&
      this.downloading.filter(
        (downloadItem) => downloadItem.comic.id === task.comic.id
      ).length === 1
    ) {
      const comic_folder = path.dirname(task.savePath);
      // if user add a new episode of this comic during zip
      // it is highly possible fail
      // the good news is we catch it, the program will not crash
      zipDirectory(comic_folder, comic_folder + ".7z", () => {
        this.downloading.splice(index, 1);
        this.complete.push(task);
        this.DownloadLoader();
        this.sendComplete();
        this.sendDownloading();
      });
    } else if (this.config.zip_options === "zip_episode") {
      // zip this episode
      zipDirectory(task.savePath, task.savePath + ".7z", () => {
        this.downloading.splice(index, 1);
        this.complete.push(task);
        this.DownloadLoader();
        this.sendComplete();
        this.sendDownloading();
      });
    } else {
      this.downloading.splice(index, 1);
      this.complete.push(task);
      this.DownloadLoader();
      this.sendComplete();
      this.sendDownloading();
    }
  }

  /**
   * Registers a download task.
   * @param task The download task to register.
   */
  public registerTask(
    task: TaskItem<ComicEpisodeObject | ComicPlusItemObject>
  ) {
    if (!this.register[task.comic.id]) {
      this.register[task.comic.id] = {};
    }
    this.register[task.comic.id][task.episode.id] = true;
  }

  /**
   * Sends the list of pending download items.
   */
  public sendPending() {
    this.emit("PendingList", this.pending);
  }

  /**
   * Sends the list of currently downloading items.
   */
  public sendDownloading() {
    this.emit("DownloadingList", this.downloading.map((downloadItem) => ({
      ...downloadItem,
      item: [],
      })));
  }

  /**
   * Sends the list of complete download items.
   */
  public sendComplete() {
    this.emit("CompleteList", this.complete);
  }

  /**
   * Sends the download list for a specific comic.
   * @param comicId The ID of the comic.
   */
  public sendRegister(comicId: number) {
    this.emit("DownloadList", this.register[comicId] ? this.register[comicId] : {});
    console.log(this.register[comicId] ? this.register[comicId] : {})
  }

  /**
   * Updates the configuration options.
   * @param newConfig The new configuration options.
   */
  public updateConfig(newConfig: Partial<typeof this.config>) {
    for (const key in newConfig) {
      this.config[key] = newConfig[key];
    }
    this.DownloadLoader();
  }
}
