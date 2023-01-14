import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import {
  BilibiliResponse,
  ComicDetailData,
  ComicPlusData,
  ImageIndexData,
  ImageTokenData,
} from "./types";

export class BilibiliMangaAPI {
  private _apiBaseUrl: string;
  private _authToken?: string;

  constructor({
    apiBaseUrl = "https://manga.bilibili.com/twirp/comic.v1.Comic",
    authToken,
  }: {
    apiBaseUrl?: string;
    authToken?: string;
  } = {}) {
    this._apiBaseUrl = apiBaseUrl;
    this._authToken = authToken;
  }

  public updateConfig({
    apiBaseUrl,
    authToken,
  }: {
    apiBaseUrl?: string;
    authToken?: string;
  }) {
    this._apiBaseUrl = apiBaseUrl !== undefined ? apiBaseUrl : this._apiBaseUrl;
    this._authToken = authToken !== undefined ? authToken : this._authToken;
    console.log(this._authToken);
  }

  public async getComicDetail(comicId: number) {
    const endpoint = "ComicDetail";
    const body = {
      comic_id: comicId,
    };
    const params = { device: "pc" };
    return this.fetch<BilibiliResponse<ComicDetailData>>({
      endpoint,
      body,
      params,
    });
  }

  public async getComicAlbumPlus(comicId: number) {
    const endpoint = "GetComicAlbumPlus";
    const body = {
      comic_id: comicId,
    };
    const params = { platform: "ios", version: 41 };
    return this.fetch<BilibiliResponse<ComicPlusData>>({
      endpoint,
      body,
      params,
    });
  }

  public async getImageIndex(episodeId: number) {
    const endpoint = "GetImageIndex";
    const body = {
      ep_id: episodeId,
    };
    const params = { device: "pc" };
    return this.fetch<BilibiliResponse<ImageIndexData>>({
      endpoint,
      body,
      params,
    });
  }

  public async getImageToken(imageUrls: string[]) {
    const endpoint = "ImageToken";
    const body = {
      urls: JSON.stringify(imageUrls),
    };
    const params = {
      platform: "web",
    };
    return this.fetch<BilibiliResponse<ImageTokenData[]>>({
      endpoint,
      body,
      params,
    });
  }

  private async fetch<T>({
    endpoint,
    body,
    params,
  }: {
    endpoint: string;
    body: object;
    params?: object;
  }): Promise<AxiosResponse<T>> {
    const axiosConfig: AxiosRequestConfig = {
      headers: {
        "Content-Type": "application/json",
        Cookie: this._authToken ? `SESSDATA=${this._authToken}` : "",
      },
      withCredentials: true,
      params: params,
    };
    console.log(axiosConfig);
    const url = `${this._apiBaseUrl}/${endpoint}`;
    return axios.post(url, body, axiosConfig);
  }
}
