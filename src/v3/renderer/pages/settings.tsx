import { useEffect, useState } from "react";
import { ipcRenderer } from "electron";
import {
  Box,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormLabel,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import Loading from "../components/Loading";
import PopoutAlert from "../components/PopoutAlert";

const Settings = () => {
  const [config, setConfig] = useState(null);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    ipcRenderer.on("CurrentConfig", (_event, args) => setConfig(args));
    ipcRenderer.send("getCurrentConfig");
    return () => {
      ipcRenderer.removeAllListeners("CurrentConfig");
    };
  }, []);
  return (
    <>
      {!config ? (
        <Loading />
      ) : (
        <Box
          display="flex"
          justifyContent="top"
          alignItems="left"
          flexDirection={"column"}
          sx={{ p: 3 }}
        >
          <PopoutAlert
            severity={"success"}
            open={open}
            handleClose={() => setOpen(false)}
          >
            设置已更新
          </PopoutAlert>
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
              onClick={() => ipcRenderer.send("openBilibiliManga")}
              color={"info"}
            >
              点此登录获取Token
            </Button>
          </Box>
          <Box display={"flex"} sx={{ mt: 3 }}>
            <TextField
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
            label="图片名称格式"
            variant="standard"
            value={config.image_file_format}
            onChange={(event) => {
              config.image_file_format = event.target.value;
              setConfig({ ...config });
            }}
            sx={{ mt: 3 }}
          />
          <Box sx={{ mt: 3 }}>
            <FormControl>
              <FormLabel id="seperate-checkbox-label">文件夹路径</FormLabel>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={config.seperate_folder}
                    onChange={(event) => {
                      config.seperate_folder = event.target.checked;
                      setConfig({ ...config });
                    }}
                  />
                }
                label="分离特典文件夹与正篇文件夹"
                aria-labelledby="seperate-checkbox-label"
              />
            </FormControl>
          </Box>
          <TextField
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
            <FormControl>
              <FormLabel id="zip-radio-buttons-group-label">压缩策略</FormLabel>
              <RadioGroup
                aria-labelledby="zip-radio-buttons-group-label"
                value={config.zip_options}
                onChange={(event) => {
                  config.zip_options = event.target.value;
                  setConfig({ ...config });
                }}
              >
                <FormControlLabel
                  value={"no_zip"}
                  control={<Radio />}
                  label="不压缩"
                />
                <FormControlLabel
                  value={"zip_comic"}
                  control={<Radio />}
                  label="整部漫画下载完成后压缩漫画文件夹"
                />
                <FormControlLabel
                  value={"zip_episode"}
                  control={<Radio />}
                  label="每话漫画下载完成后压缩单话文件夹"
                />
              </RadioGroup>
            </FormControl>
          </Box>
          <Box sx={{ mt: 3 }}>
            <FormControl>
              <FormLabel id="metadata-select-label">元数据</FormLabel>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={config.save_meta_data}
                    onChange={(event) => {
                      config.save_meta_data = event.target.checked;
                      setConfig({ ...config });
                    }}
                  />
                }
                label="自动保存tachiyomi元数据"
                aria-labelledby="metadata-radio-buttons-group-label"
              />
            </FormControl>
          </Box>
          <Box sx={{ mt: 3 }}>
            <FormControl>
              <FormLabel id="close-radio-buttons-group-label">
                关闭主界面
              </FormLabel>
              <RadioGroup
                aria-labelledby="close-radio-buttons-group-label"
                value={config.hide_in_tray}
                onChange={(event) => {
                  config.hide_in_tray = JSON.parse(event.target.value);
                  setConfig({ ...config });
                }}
              >
                <FormControlLabel
                  value={true}
                  control={<Radio />}
                  label="最小化到系统托盘"
                />
                <FormControlLabel
                  value={false}
                  control={<Radio />}
                  label="退出程序"
                />
              </RadioGroup>
            </FormControl>
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
