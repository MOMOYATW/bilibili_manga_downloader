import { BilibiliMangaAPI } from "../bilibili-manga-client";
import { config } from "./configHandler";

export const api = new BilibiliMangaAPI({ authToken: config.get('token') });

export async function handleGetSearch(event: Electron.IpcMainEvent, searchContent: string) {
    try {
        const result = await api.getSearch(searchContent);
        event.sender.send("Search", result.data.data.list);
    } catch (error) {
        console.log(error);
        event.sender.send("Search", []);
    }
}

export async function handleGetComicDetail(event: Electron.IpcMainEvent, comicId: number) {
    try {
        const result = await api.getComicDetail(comicId);
        event.sender.send("ComicDetail", result.data.data);
    } catch (error) {
        console.log(error);
        event.sender.send("ComicDetail", null);
    }
}

export async function handleGetComicAlbumPlus(event: Electron.IpcMainEvent, comicId: number) {
    try {
        const result = await api.getComicAlbumPlus(comicId);
        event.sender.send("ComicAlbumPlus", result.data.data);
    } catch (error) {
        console.log(error);
        event.sender.send("ComicAlbumPlus", null);
    }
}