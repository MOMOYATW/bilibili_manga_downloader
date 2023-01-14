import {
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  CardMedia,
  Box,
  LinearProgress,
  MenuItem,
  ListItemIcon,
  Menu,
} from "@mui/material";
import React, { useState } from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import { useRouter } from "next/router";
import { ComicListItem } from "../types";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import FolderIcon from "@mui/icons-material/Folder";
import FolderZipIcon from "@mui/icons-material/FolderZip";
import ShortcutIcon from "@mui/icons-material/Shortcut";
import path from "path";
import { ipcRenderer } from "electron";

const DownloadList = ({
  downloadList,
  type,
  onDelete,
  detail,
}: {
  downloadList: ComicListItem[];
  type: "PendingList" | "DownloadingList" | "CompleteList";
  onDelete: Function;
  detail?: boolean;
}) => {
  const router = useRouter();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [index, setIndex] = useState<number>(0);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const menuItems = [
    {
      name: "移除",
      icon: <DeleteIcon fontSize="small" />,
      function: () => {
        onDelete(
          detail ? downloadList[index].episode.id : downloadList[index].comic.id
        );
        handleClose();
      },
    },
    {
      name: "转到漫画页面",
      icon: <ShortcutIcon fontSize="small" />,
      function: () => {
        router.push(
          {
            pathname: `/comics/${downloadList[index].comic.id}`,
          },
          undefined,
          { shallow: true }
        );
      },
    },
    {
      name: "打开文件夹",
      icon: <FolderIcon fontSize="small" />,
      function: () => {
        if (detail) {
          require("electron").shell.openPath(downloadList[index].savePath);
        } else {
          const comicFolder = path.join(
            ...downloadList[index].savePath
              .split(path.sep)
              .splice(
                0,
                downloadList[index].savePath.split(path.sep).length - 1
              )
          );
          require("electron").shell.openPath(comicFolder);
        }

        handleClose();
      },
    },
    {
      name: "压缩",
      icon: <FolderZipIcon fontSize="small" />,
      function: () => {
        const comicFolder = path.join(
          ...downloadList[index].savePath
            .split(path.sep)
            .splice(0, downloadList[index].savePath.split(path.sep).length - 1)
        );
        ipcRenderer.send("zipFolder", comicFolder);
        console.log(comicFolder);
        handleClose();
      },
    },
  ];

  const getProgressValue = (item: ComicListItem) => {
    if (type === "PendingList") return 0;
    if (type === "DownloadingList") return item.progress;
    if (type === "CompleteList") return 100;
  };
  return (
    <List
      sx={{
        width: "100%",
        bgcolor: "background.paper",
      }}
    >
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
      >
        {menuItems
          .slice(0, type === "CompleteList" ? 4 - (detail ? 1 : 0) : 2)
          .map((item, index) => {
            return (
              <MenuItem onClick={item.function} key={index}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText>{item.name}</ListItemText>
              </MenuItem>
            );
          })}
      </Menu>
      {downloadList.length !== 0 ? (
        downloadList.map((downloadItem, index) => {
          const id = detail ? downloadItem.episode.id : downloadItem.comic.id;
          return (
            <ListItem
              key={id}
              secondaryAction={
                <IconButton
                  edge="end"
                  aria-label="comments"
                  onClick={(event) => {
                    setIndex(index);
                    handleClick(event);
                  }}
                >
                  {<ExpandMoreIcon />}
                </IconButton>
              }
              disablePadding
            >
              <ListItemButton
                role={undefined}
                onClick={() => {
                  router.push(
                    {
                      pathname: `/${type
                        .slice(0, type.length - 4)
                        .toLowerCase()}/${downloadItem.comic.id}`,
                    },
                    undefined,
                    { shallow: true }
                  );
                }}
              >
                <Box width={"250px"} sx={{ mr: 1 }}>
                  <CardMedia
                    component="img"
                    image={downloadItem.comic.cover}
                    alt="Cover"
                  />
                </Box>
                <Box display={"flex"} flexDirection={"column"} width="100%">
                  <ListItemText
                    primary={
                      detail
                        ? downloadItem.episode.title
                        : downloadItem.comic.title
                    }
                    secondary={
                      downloadItem.task_cnt
                        ? `任务数量：${downloadItem.task_cnt}`
                        : null
                    }
                  />
                  <LinearProgress
                    variant="determinate"
                    value={getProgressValue(downloadItem)}
                    color={"warning"}
                  />
                </Box>
              </ListItemButton>
            </ListItem>
          );
        })
      ) : (
        <Box>还没有内容哟~快去下载吧！</Box>
      )}
    </List>
  );
};

export default DownloadList;
