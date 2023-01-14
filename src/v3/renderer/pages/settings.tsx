import {
  Alert,
  Box,
  Button,
  IconButton,
  Select,
  Snackbar,
  Switch,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { ipcRenderer } from "electron";
import { useEffect, useState } from "react";
import Loading from "../components/Loading";

const Settings = () => {
  const [config, setConfig] = useState(null);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    ipcRenderer.on("CurrentConfig", (event, args) => {
      setConfig(args);
    });
    ipcRenderer.send("getCurrentConfig");
    return () => {
      ipcRenderer.removeAllListeners("CurrentConfig");
    };
  }, []);
  return (
    <>
      {!config ? (
        <Loading failed={false} />
      ) : (
        <Box
          display="flex"
          justifyContent="top"
          alignItems="left"
          flexDirection={"column"}
          sx={{ p: 3 }}
        >
          <Snackbar
            open={open}
            autoHideDuration={3000}
            onClose={() => setOpen(false)}
            anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          >
            <Alert
              severity="success"
              action={
                <IconButton
                  aria-label="close"
                  color="inherit"
                  size="small"
                  onClick={() => {
                    setOpen(false);
                  }}
                >
                  <CloseIcon fontSize="inherit" />
                </IconButton>
              }
              sx={{ mb: 2 }}
            >
              设置已更新
            </Alert>
          </Snackbar>
          <Typography
            variant="h5"
            component="div"
            fontWeight={"bold"}
            sx={{ mb: 2, mt: 2 }}
          >
            设置
          </Typography>
          <Box display={"flex"}>
            <TextField
              id="standard-basic"
              label="Token"
              variant="standard"
              value={config.token}
              onChange={(event) => {
                config.token = event.target.value;
                setConfig({ ...config });
              }}
              sx={{ width: "85%" }}
            />
            <Button
              sx={{ ml: 1 }}
              onClick={() => {
                require("electron").shell.openExternal(
                  "https://github.com/MOMOYATW/bilibili_manga_downloader#%E6%9C%89%E5%85%B3%E4%BA%8E%E7%99%BB%E5%BD%95-cookie-%E7%9A%84%E8%8E%B7%E5%8F%96"
                );
              }}
              color={"info"}
            >
              如何获取Token?
            </Button>
          </Box>
          <Box display={"flex"} sx={{ mt: 3 }}>
            <TextField
              id="standard-basic"
              label="下载路径"
              variant="standard"
              value={config.download_path}
              sx={{ width: "85%" }}
              disabled
            />
            <Button
              variant="contained"
              component="label"
              sx={{ ml: 1 }}
              onClick={() => {
                ipcRenderer.send("openDialog");
              }}
            >
              选择路径
            </Button>
          </Box>
          <TextField
            id="standard-basic"
            label="漫画文件夹名称格式"
            variant="standard"
            value={config.comic_folder_format}
            onChange={(event) => {
              config.comic_folder_format = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <TextField
            id="standard-basic"
            label="每话文件夹名称格式"
            variant="standard"
            value={config.episode_folder_format}
            onChange={(event) => {
              config.episode_folder_format = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <TextField
            id="standard-basic"
            label="特典文件夹名称格式"
            variant="standard"
            value={config.tokuten_folder_format}
            onChange={(event) => {
              config.tokuten_folder_format = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <TextField
            id="standard-basic"
            label="图片名称格式"
            variant="standard"
            value={config.image_file_format}
            onChange={(event) => {
              config.image_file_format = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <TextField
            id="standard-basic"
            label="同时下载集数"
            variant="standard"
            type={"number"}
            value={config.max_download_num}
            onChange={(event) => {
              config.max_download_num = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <Box sx={{ mt: 3 }}>
            下载完成后压缩
            <Tooltip title="开启后会影响下载速度" arrow>
              <Switch
                checked={config.zip_after_download}
                onChange={(event) => {
                  config.zip_after_download = event.target.checked;
                  setConfig({ ...config });
                }}
              />
            </Tooltip>
          </Box>
          <Button
            onClick={() => {
              ipcRenderer.send("updateConfig", config);
              setOpen(true);
            }}
            sx={{ mt: 3, mb: 3 }}
            color={"info"}
          >
            保存设置
          </Button>
        </Box>
      )}
    </>
  );
};

export default Settings;
