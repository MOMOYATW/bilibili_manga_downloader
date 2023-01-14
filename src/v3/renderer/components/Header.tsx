import {
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Avatar,
} from "@mui/material";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import RemoveIcon from "@mui/icons-material/Remove";
import CloseIcon from "@mui/icons-material/Close";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import CloseFullscreenIcon from "@mui/icons-material/CloseFullscreen";
import React, { useState, useEffect } from "react";
import styles from "../styles/Header.module.css";

import { ipcRenderer } from "electron";

const Header = ({ toggleTheme, theme }) => {
  const [maximum, setMaximum] = useState(false);
  useEffect(() => {
    ipcRenderer.on("isMaximized", (event, args) => {
      setMaximum(true);
    });
    ipcRenderer.on("isRestored", (event, args) => {
      setMaximum(false);
    });
  }, []);

  return (
    <AppBar
      position="fixed"
      sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      className={styles.drag_region}
    >
      <Toolbar variant="dense" sx={{ minHeight: 0 }} disableGutters>
        <Avatar
          alt="Bilibli Manga Downloader"
          src="/images/logo.png"
          sx={{ width: 30, height: 30, ml: 2, mr: 2 }}
        />
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            fontWeight: "bold",
            fontSize: "0.9rem",
          }}
        >
          哔哩哔哩漫画下载器
        </Typography>
        <div className={styles.window_controls}>
          <IconButton
            size="small"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={toggleTheme}
            sx={{ mr: 1, ml: 1 }}
          >
            {theme === "light" ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
          <Button
            color="inherit"
            onClick={() => ipcRenderer.send("minimiseApp")}
          >
            <RemoveIcon />
          </Button>
          <Button
            color="inherit"
            onClick={() => ipcRenderer.send("maximizeRestoreApp")}
          >
            {maximum ? <CloseFullscreenIcon /> : <OpenInFullIcon />}
          </Button>
          <Button
            color="inherit"
            id={styles.closeBtn}
            onClick={() => ipcRenderer.send("closeApp")}
          >
            <CloseIcon />
          </Button>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
