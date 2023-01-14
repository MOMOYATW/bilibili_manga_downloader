import { ipcRenderer } from "electron";
import { Box, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import {
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "../../main/bilibili-manga-client";
import { TaskItem } from "../../main/types";
import { ComicListItem } from "../types";
import DownloadList from "./DownloadList";

const TaskSets = ({
  taskType,
  operateName,
  pageTitle,
}: {
  taskType: "PendingList" | "DownloadingList" | "CompleteList";
  operateName: "cancel" | "delete";
  pageTitle: string;
}) => {
  const [taskList, setTaskComicList] = useState<ComicListItem[]>([]);
  const loadData = () => {
    ipcRenderer.send("get" + taskType);
  };
  useEffect(() => {
    ipcRenderer.on(
      taskType,
      (event, args: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[]) => {
        const taskComicList: ComicListItem[] = [];
        args.map((taskItem) => {
          const existItem = taskComicList.filter(
            (listItem) => listItem.comic.id === taskItem.comic.id
          )[0];
          if (!existItem)
            taskComicList.push({
              ...taskItem,
              task_cnt: 1,
            });
          else existItem.task_cnt += 1;
        });
        setTaskComicList(taskComicList);
      }
    );
    loadData();
    return () => {
      ipcRenderer.removeAllListeners(taskType);
    };
  }, []);
  return (
    <Box
      display="flex"
      justifyContent="top"
      alignItems="left"
      flexDirection={"column"}
      sx={{ height: "100%", p: 3 }}
    >
      <Typography
        variant="h5"
        component="div"
        fontWeight={"bold"}
        sx={{ mb: 2, mt: 2 }}
      >
        {pageTitle}
      </Typography>
      <DownloadList
        downloadList={taskList}
        type={taskType}
        onDelete={(deleteId: number) => {
          ipcRenderer.send(
            operateName + "Comic" + taskType.slice(0, taskType.length - 4),
            deleteId
          );
        }}
      ></DownloadList>
    </Box>
  );
};

export default TaskSets;
