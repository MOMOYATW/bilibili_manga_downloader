import {
  Box,
  Typography,
  ListItemButton,
  Chip,
  Snackbar,
  Alert,
  IconButton,
  AlertColor,
} from "@mui/material";
import React, { useState } from "react";
import Image from "next/image";
import GitHubIcon from "@mui/icons-material/GitHub";
import RssFeedIcon from "@mui/icons-material/RssFeed";
import CloseIcon from "@mui/icons-material/Close";
import axios from "axios";

const About = () => {
  const major_version = 3;
  const minor_version = 0;
  const patch_version = 1;
  const pre_release = false;
  const [snackBar, setSnackBar] = useState<{
    open: boolean;
    text: string;
    color: AlertColor;
  }>({
    open: false,
    text: "",
    color: "success",
  });
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={"column"}
      sx={{ height: "100%" }}
    >
      <Snackbar
        open={snackBar.open}
        autoHideDuration={3000}
        onClose={() => setSnackBar({ ...snackBar, open: false })}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      >
        <Alert
          severity={snackBar.color}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setSnackBar({ ...snackBar, open: false });
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          {snackBar.text}
        </Alert>
      </Snackbar>
      <Box sx={{ flexGrow: 0.5 }}></Box>
      <ListItemButton
        sx={{ flexGrow: 0 }}
        onClick={() => {
          require("electron").shell.openExternal(
            "https://github.com/MOMOYATW/bilibili_manga_downloader"
          );
        }}
      >
        <Image src={"/images/logo.png"} width={80} height={80} />
      </ListItemButton>

      <Typography
        variant="h5"
        component="div"
        fontWeight={"bold"}
        sx={{ mt: 2 }}
      >
        哔哩哔哩漫画下载器
      </Typography>
      <Chip
        label={
          `v ${major_version}.${minor_version}.${patch_version} ` +
          (pre_release ? "pre-release" : "")
        }
        color="primary"
        onClick={() => {
          axios
            .get(
              "https://api.github.com/repos/MOMOYATW/bilibili_manga_downloader/releases/latest"
            )
            .then((result) => {
              console.log(result.data.tag_name);
              const [
                latest_major_version,
                latest_minor_version,
                latest_patch_version,
              ] = result.data.tag_name
                .slice(1)
                .split(".")
                .map((version) => +version);
              if (
                latest_major_version > major_version ||
                (latest_major_version === major_version &&
                  latest_minor_version > major_version) ||
                (latest_major_version === major_version &&
                  latest_minor_version === minor_version &&
                  latest_patch_version > patch_version)
              ) {
                setSnackBar({
                  open: true,
                  text: "查询到新版本",
                  color: "info",
                });
              } else {
                setSnackBar({
                  open: true,
                  text: "已是最新版本",
                  color: "success",
                });
              }
            });
        }}
      />
      <Box sx={{ flexGrow: 1 }}></Box>
      <Box sx={{ display: "flex", mb: 3 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            mr: 1,
          }}
        >
          基于
        </Box>

        <ListItemButton
          sx={{ flexDirection: "column" }}
          onClick={() => {
            require("electron").shell.openExternal("https://nextjs.org/");
          }}
        >
          <Image
            src={"https://cdn.worldvectorlogo.com/logos/next-js.svg"}
            width={40}
            height={40}
          />
          Next.js
        </ListItemButton>
        <ListItemButton
          sx={{ flexDirection: "column" }}
          onClick={() => {
            require("electron").shell.openExternal("https://mui.com/");
          }}
        >
          <Image
            src={"https://cdn.worldvectorlogo.com/logos/material-ui-1.svg"}
            width={40}
            height={40}
          />
          Material UI
        </ListItemButton>
        <ListItemButton
          sx={{ flexDirection: "column" }}
          onClick={() => {
            require("electron").shell.openExternal(
              "https://www.electronjs.org/"
            );
          }}
        >
          <Image
            src={"https://www.electronjs.org/assets/img/logo.svg"}
            width={40}
            height={40}
          />
          Electron
        </ListItemButton>
      </Box>
      <Box sx={{ display: "flex", mb: 3 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            mr: 1,
          }}
        >
          关于我
        </Box>
        <ListItemButton
          onClick={() => {
            require("electron").shell.openExternal(
              "https://github.com/MOMOYATW"
            );
          }}
        >
          <GitHubIcon fontSize="large" />
        </ListItemButton>
        <ListItemButton
          onClick={() => {
            require("electron").shell.openExternal("https://blog.davytao.me/");
          }}
        >
          <RssFeedIcon fontSize="large" />
        </ListItemButton>
      </Box>
    </Box>
  );
};

export default About;
