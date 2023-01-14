import {
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import { DownloadItemsMapping, TaskItem } from "./types";

export class MappingManager {
  downloadItemsMapping: DownloadItemsMapping;
  constructor() {
    this.downloadItemsMapping = {};
  }
  public recordExist(serverSideName: string): boolean {
    const mappingInfos = this.downloadItemsMapping[serverSideName];
    if (mappingInfos === undefined) {
      return false;
    }
    return true;
  }

  public getMappingInfo(
    serverSideName: string,
    downloadingList: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[]
  ): { episodeId: number; filename: string } {
    if (!this.recordExist(serverSideName))
      throw Error("Always check recordExist before call this function");
    const mappingInfos = this.downloadItemsMapping[serverSideName];

    if (mappingInfos.length === 1) {
      const mappingInfo = mappingInfos.pop();
      delete this.downloadItemsMapping[serverSideName];
      return mappingInfo;
    } else {
      // find which one is downloading
      const downloadingMappingInfos = mappingInfos.filter((mappingInfo) => {
        return (
          downloadingList.filter((downloadItem) => {
            return downloadItem.episode.id === mappingInfo.episodeId;
          }).length >= 1
        );
      });
      const mappingInfo = downloadingMappingInfos.pop();
      const index = mappingInfos.indexOf(mappingInfo);
      mappingInfos.splice(index, 1);
      return mappingInfo;
    }
  }

  public registerMappingInfo(
    serverSideName: string,
    mappingInfo: { episodeId: number; filename: string }
  ) {
    if (!this.recordExist(serverSideName)) {
      this.downloadItemsMapping[serverSideName] = [];
      this.downloadItemsMapping[serverSideName].push(mappingInfo);
    } else {
      const exist =
        this.downloadItemsMapping[serverSideName].indexOf(mappingInfo);
      if (exist === -1) {
        this.downloadItemsMapping[serverSideName].push(mappingInfo);
      } else {
        console.warn("There is a duplicate Mapping record try to register");
      }
    }
  }
}
