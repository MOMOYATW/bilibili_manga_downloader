import { Dispatch, SetStateAction, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Collapse,
  Grid,
  IconButton,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import {
  ComicEpisodeObject,
  ComicPlusItemObject,
  ComicPlusObject,
  TaskItem,
} from "../types";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ViewCompactIcon from "@mui/icons-material/ViewCompact";
import WindowIcon from "@mui/icons-material/Window";

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
  const [expanded, setExpanded] = useState(true);
  const [compact, setCompact] = useState(false);
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
  const getTitle = (
    episode: ComicEpisodeObject | ComicPlusObject,
    compact = false
  ) => {
    if ("item" in episode) {
      return episode.item.title;
    }
    return episode.short_title + (compact ? "" : " " + episode.title);
  };
  return (
    <Card sx={{ p: 2, mt: 2 }}>
      <CardActions disableSpacing>
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
        <Box sx={{ flexGrow: 1 }}></Box>
        <IconButton aria-label="compact" onClick={() => setCompact(!compact)}>
          {compact ? <WindowIcon /> : <ViewCompactIcon />}
        </IconButton>
        <IconButton aria-label="expand" onClick={() => setExpanded(!expanded)}>
          <ExpandMoreIcon
            style={{
              transform: !expanded ? "rotate(0deg)" : "rotate(180deg)",
              transition: "all 0.2s",
            }}
          />
        </IconButton>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent sx={{ width: "100%" }}>
          <Grid
            container
            rowSpacing={1}
            columnSpacing={{ xs: 1, sm: 2, md: 3 }}
          >
            {episodeList.map((episode, index) => {
              return (
                <Grid
                  item
                  xs={compact ? 3 : 6}
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
                      primary={getTitle(episode, compact)}
                      secondary={judgeCurrentState(episode)}
                    />
                  </ListItemButton>
                </Grid>
              );
            })}
          </Grid>
        </CardContent>
      </Collapse>
    </Card>
  );
};

export default EpisodeList;
