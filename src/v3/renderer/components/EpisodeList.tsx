import {
  Button,
  Card,
  CardContent,
  Grid,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import React, { Dispatch, SetStateAction } from "react";
import {
  ComicEpisodeObject,
  ComicPlusItemObject,
  ComicPlusObject,
} from "../../main/bilibili-manga-client";
import { TaskItem } from "../../main/types";

const EpisodeList = ({
  selectedEpisodeIndex,
  episodeList,
  setSelectedEpisodeIndex,
  downloadList,
}: {
  selectedEpisodeIndex: number[];
  episodeList: any[];
  setSelectedEpisodeIndex: Dispatch<SetStateAction<number[]>>;
  downloadList: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[];
}) => {
  const judgeCurrentState = (episode: ComicEpisodeObject | ComicPlusObject) => {
    if ("item" in episode) {
      if (downloadList[episode.item.id]) {
        return "已在下载列表";
      }
      if (episode.isLock) return "下线时间：" + episode.item.offline_time;
      return "已解锁";
    }
    if (downloadList[episode.id]) {
      return "已在下载列表";
    }
    if (episode.is_locked) return "价格: " + episode.pay_gold;
    return "已解锁";
  };
  const judgeCurrentDisable = (
    episode: ComicEpisodeObject | ComicPlusObject
  ) => {
    if ("item" in episode) {
      if (downloadList[episode.item.id]) {
        return true;
      }
      if (episode.isLock) return true;
      return false;
    }
    if (downloadList[episode.id]) {
      return true;
    }
    if (episode.is_locked) return true;
    return false;
  };
  const getTitle = (episode: ComicEpisodeObject | ComicPlusObject) => {
    if ("item" in episode) {
      return episode.item.title;
    }
    return episode.short_title + " " + episode.title;
  };
  return (
    <Card sx={{ display: "flex", p: 2, mt: 2 }}>
      <CardContent sx={{ width: "100%" }}>
        <Button
          size="large"
          sx={{ mb: 1 }}
          color={"info"}
          onClick={() => {
            if (
              selectedEpisodeIndex.length !==
              episodeList.filter((episode) => !judgeCurrentDisable(episode))
                .length
            ) {
              setSelectedEpisodeIndex(
                episodeList
                  .filter((episode) => !judgeCurrentDisable(episode))
                  .map((episode) => episodeList.indexOf(episode))
              );
            } else {
              setSelectedEpisodeIndex([]);
            }
          }}
        >
          {selectedEpisodeIndex.length !==
          episodeList.filter((episode) => !judgeCurrentDisable(episode)).length
            ? "全选"
            : "全不选"}
        </Button>
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          {episodeList.map((episode, index) => {
            return (
              <Grid
                item
                xs={6}
                key={"item" in episode ? episode.item.id : episode.id}
              >
                <ListItemButton
                  selected={selectedEpisodeIndex.includes(index)}
                  onClick={() => {
                    const findIndex = selectedEpisodeIndex.indexOf(index);
                    if (findIndex !== -1) {
                      selectedEpisodeIndex.splice(findIndex, 1);
                    } else {
                      selectedEpisodeIndex.push(index);
                    }
                    setSelectedEpisodeIndex([...selectedEpisodeIndex]);
                  }}
                  disabled={judgeCurrentDisable(episode)}
                >
                  <ListItemText
                    primary={getTitle(episode)}
                    secondary={judgeCurrentState(episode)}
                  />
                </ListItemButton>
              </Grid>
            );
          })}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default EpisodeList;
