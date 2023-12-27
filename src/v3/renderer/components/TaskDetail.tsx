import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { ipcRenderer } from "electron";
import { Box, Typography } from "@mui/material";
import DownloadList from "./DownloadList";
import {
  ComicListItem,
  TaskItem,
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "../types";

const TaskDetail = ({
  taskType,
  operateName,
}: {
  taskType: "PendingList" | "DownloadingList" | "CompleteList";
  operateName: "cancel" | "delete";
}) => {
  const router = useRouter();
  const comicId = +router.query["id"];
  const [taskEpisodeList, setTaskEpisodeList] = useState<ComicListItem[]>([]);
  const [comicTitle, setComicTitle] = useState("");
  const loadData = () => {
    ipcRenderer.send("get" + taskType);
  };
  useEffect(() => {
    ipcRenderer.on(
      taskType,
      (event, args: TaskItem<ComicEpisodeObject | ComicPlusItemObject>[]) => {
        const episode_list: ComicListItem[] = args.filter(
          (taskItem) => taskItem.comic.id === comicId
        );
        if (episode_list.length === 0) {
          router.push(
            {
              pathname: `/${taskType
                .slice(0, taskType.length - 4)
                .toLowerCase()}/`,
            },
            undefined,
            { shallow: true }
          );
        }
        setTaskEpisodeList(episode_list);
        setComicTitle(
          args?.filter((item) => item.comic.id === comicId)[0]?.comic.title
        );
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
        {comicTitle} 的任务详情
      </Typography>
      <DownloadList
        downloadList={taskEpisodeList}
        type={taskType}
        onDelete={(itemId: number) => {
          ipcRenderer.send(
            operateName + "Episode" + taskType.slice(0, taskType.length - 4),
            itemId
          );
          ipcRenderer.send("get" + taskType);
        }}
        detail
      ></DownloadList>
    </Box>
  );
};

export default TaskDetail;
