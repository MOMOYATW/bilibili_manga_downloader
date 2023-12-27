import {
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "../../main/bilibili-manga-client";
import { TaskItem } from "../../main/types";

export interface ComicListItem
  extends TaskItem<ComicEpisodeObject | ComicPlusItemObject> {
  task_cnt?: number;
}

export * from "../../main/bilibili-manga-client";
export * from "../../main/types";
