import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { ipcRenderer } from "electron";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardMedia,
  Chip,
  Typography,
  Divider,
  Snackbar,
  Alert,
  IconButton,
} from "@mui/material";
import EpisodeList from "../../components/EpisodeList";
import Loading from "../../components/Loading";
import CloseIcon from "@mui/icons-material/Close";
import {
  ComicDetailData,
  ComicEpisodeObject,
  ComicPlusData,
  ComicPlusItemObject,
} from "../../../main/bilibili-manga-client";
import { TaskItem } from "../../../main/types";

const ComicDetail = () => {
  const router = useRouter();
  const [comicInfo, setComicInfo] = useState<ComicDetailData | null>(null);
  const [selectedEpisodeIndex, setSelectedEpisodeIndex] = useState<number[]>(
    []
  );
  const [comicPlusInfo, setComicPlusInfo] = useState<ComicPlusData | null>(
    null
  );
  const [selectedPlusIndex, setSelectPlusInex] = useState<number[]>([]);
  const [downloadList, setDownloadList] = useState<
    TaskItem<ComicEpisodeObject | ComicPlusItemObject>[]
  >([]);
  const [failed, setFailed] = useState(false);
  const [open, setOpen] = useState(false);
  const loadData = () => {
    ipcRenderer.send("getComicDetail", router.query["id"]);
    ipcRenderer.send("getComicAlbumPlus", router.query["id"]);
    ipcRenderer.send("getDownloadList", router.query["id"]);
  };
  useEffect(() => {
    ipcRenderer.on("ComicDetail", (_event, args: ComicDetailData) => {
      if (args === null) {
        setFailed(true);
        return;
      }
      args.ep_list.reverse();
      setComicInfo(args);
    });
    ipcRenderer.on("ComicAlbumPlus", (_event, args) => {
      setComicPlusInfo(args);
    });
    ipcRenderer.on("DownloadList", (_event, args) => {
      setDownloadList(args);
      console.log(args);
    });
    loadData();
    return () => {
      ipcRenderer.removeAllListeners("ComicDetail");
      ipcRenderer.removeAllListeners("ComicAlbumPlus");
      ipcRenderer.removeAllListeners("DownloadList");
    };
  }, []);

  return (
    <>
      {!comicInfo ? (
        <Loading failed={failed} />
      ) : (
        <Box display="flex" flexDirection={"column"} sx={{ p: 3 }}>
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
              任务已添加
            </Alert>
          </Snackbar>
          <Card
            sx={{
              display: "flex",
              p: 2,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <CardMedia
                component="img"
                sx={{
                  width: "300px",
                  p: 1,
                }}
                image={comicInfo.vertical_cover}
                alt="Vertical Cover of the Comic"
              />
            </Box>
            <Box sx={{ display: "flex", flexDirection: "column" }}>
              <CardContent>
                <Typography
                  variant="h5"
                  component="div"
                  sx={{ fontWeight: "bold" }}
                >
                  {comicInfo.title}
                </Typography>
                <Typography sx={{ mb: 1.5, mt: 1.5 }} color="text.secondary">
                  {comicInfo.author_name.map((author) => (
                    <span key={author} style={{ marginRight: 10 }}>
                      {author}
                    </span>
                  ))}
                </Typography>

                <Typography variant="body2" sx={{ lineHeight: 2 }}>
                  {comicInfo.classic_lines}
                </Typography>

                <Box sx={{ fontSize: 14, mt: 2 }} color="text.secondary">
                  {comicInfo.tags.map((tag) => (
                    <Chip
                      key={tag.id}
                      label={tag.name}
                      style={{ marginRight: 10, marginBottom: 10 }}
                    />
                  ))}
                  <Divider flexItem orientation="vertical" />
                  {comicInfo.styles2.map((tag) => (
                    <Chip
                      key={tag.id}
                      label={tag.name}
                      style={{ marginRight: 10, marginBottom: 10 }}
                    />
                  ))}
                </Box>
              </CardContent>
              <Box sx={{ flexGrow: 1 }}></Box>
              <CardActions sx={{ display: "flex" }}>
                <Button
                  size="large"
                  variant="contained"
                  onClick={() => {
                    setOpen(true);
                    const selectedEpisodes = comicInfo.ep_list.filter(
                      (_episode, index) => selectedEpisodeIndex.includes(index)
                    );
                    ipcRenderer.send("DownloadEpisodes", {
                      ...comicInfo,
                      ep_list: selectedEpisodes,
                    });
                    const selectedPlusEpisodes = comicPlusInfo.list.filter(
                      (_plusEpisode, index) => selectedPlusIndex.includes(index)
                    );
                    ipcRenderer.send("DownloadPlusEpisodes", {
                      comic: comicInfo,
                      ep_list: selectedPlusEpisodes,
                    });
                    ipcRenderer.send("getDownloadList", router.query["id"]);
                    ipcRenderer.send("getComicAlbumPlus", router.query["id"]);
                    setSelectedEpisodeIndex([]);
                  }}
                >
                  下载选中
                </Button>
                <Box sx={{ flexGrow: 1 }}></Box>
                <Button size="large" onClick={loadData} color={"info"}>
                  重新加载
                </Button>
              </CardActions>
            </Box>
          </Card>
          <EpisodeList
            selectedEpisodeIndex={selectedEpisodeIndex}
            setSelectedEpisodeIndex={setSelectedEpisodeIndex}
            episodeList={comicInfo.ep_list}
            downloadList={downloadList}
          />
          {comicPlusInfo && comicPlusInfo.list.length !== 0 && (
            <EpisodeList
              selectedEpisodeIndex={selectedPlusIndex}
              setSelectedEpisodeIndex={setSelectPlusInex}
              episodeList={comicPlusInfo.list}
              downloadList={downloadList}
            />
          )}
        </Box>
      )}
    </>
  );
};

export default ComicDetail;
