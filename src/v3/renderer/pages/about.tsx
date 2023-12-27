import React, { useEffect, useState } from "react";
import Image from "next/image";
import { ipcRenderer } from "electron";
import { Box, Typography, ListItemButton, Chip } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import RssFeedIcon from "@mui/icons-material/RssFeed";

const About = ({selectedTheme}) => {
  const [version, setVersion] = useState("");
  useEffect(() => {
    ipcRenderer.on("Version", (_event, version) => setVersion("v" + version));
    ipcRenderer.send("getVersion");
    return () => {
      ipcRenderer.removeAllListeners("Version");
    };
  });
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={"column"}
      sx={{ height: "100%" }}
    >
      <Box sx={{ flexGrow: 0.5 }}></Box>
      <ListItemButton
        sx={{ flexGrow: 0 }}
        onClick={() =>
          require("electron").shell.openExternal(
            "https://github.com/MOMOYATW/bilibili_manga_downloader"
          )
        }
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
      <Chip label={version} color="primary" />
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
          onClick={() =>
            require("electron").shell.openExternal("https://nextjs.org/")
          }
        >
          <Image src={"/images/next-js.svg"} width={40} height={40} style={{filter: selectedTheme === "light" ? "" : "invert(99%) sepia(0%) saturate(7435%) hue-rotate(188deg) brightness(119%) contrast(99%)"}}/>
          Next.js
        </ListItemButton>
        <ListItemButton
          sx={{ flexDirection: "column" }}
          onClick={() =>
            require("electron").shell.openExternal("https://mui.com/")
          }
        >
          <Image src={"/images/material-ui.svg"} width={40} height={40} />
          Material UI
        </ListItemButton>
        <ListItemButton
          sx={{ flexDirection: "column" }}
          onClick={() =>
            require("electron").shell.openExternal(
              "https://www.electronjs.org/"
            )
          }
        >
          <Image src={"/images/electron.svg"} width={40} height={40} />
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
          onClick={() =>
            require("electron").shell.openExternal(
              "https://github.com/MOMOYATW"
            )
          }
        >
          <GitHubIcon fontSize="large" />
        </ListItemButton>
        <ListItemButton
          onClick={() =>
            require("electron").shell.openExternal("https://blog.davytao.me/")
          }
        >
          <RssFeedIcon fontSize="large" />
        </ListItemButton>
      </Box>
    </Box>
  );
};

export default About;
