import { useEffect, useState } from "react";
import Head from "next/head";
import Image from "next/image";
import { useRouter } from "next/router";
import {
  Alert,
  Box,
  IconButton,
  Snackbar,
  Toolbar,
  useTheme,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import SearchBar from "../components/SearchBar";
import { ipcRenderer } from "electron";

function Home() {
  const [searchContent, setSearchContent] = useState("");
  const [open, setOpen] = useState(false);
  const router = useRouter();
  const theme = useTheme();

  useEffect(() => {
    // like componentDidMount()

    // register `ping-pong` event
    ipcRenderer.on("ping-pong", (event, data) => {
      console.log(data);
    });
    ipcRenderer.send("ping-pong", ["some data from ipcRenderer"]);
    return () => {
      // like componentWillUnmount()

      // unregister it
      ipcRenderer.removeAllListeners("ping-pong");
    };
  }, []);

  const parseSearchContent = () => {
    // check if is comic detail url
    const result_1 = searchContent.match(
      /manga\.bilibili\.com\/detail\/mc[0-9]*/
    );
    if (result_1 !== null) {
      const comicId = result_1[0].slice(28);
      router.push(
        {
          pathname: `/comics/${comicId}`,
        },
        undefined,
        { shallow: true }
      );
      return true;
    }
    // check if episode url
    const result_2 = searchContent.match(
      /manga\.bilibili\.com\/mc[0-9]*\/[0-9]*/
    );
    if (result_2 !== null) {
      const comicId = result_2[0].slice(21).split("/")[0];
      router.push(
        {
          pathname: `/comics/${comicId}`,
        },
        undefined,
        { shallow: true }
      );
      return true;
    }

    return false;
  };

  return (
    <>
      <Head>
        <title>哔哩哔哩漫画下载器</title>
      </Head>
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        flexDirection={"column"}
        sx={{ height: "100%" }}
      >
        <Snackbar
          open={open}
          autoHideDuration={3000}
          onClose={() => setOpen(false)}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        >
          <Alert
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
            severity="error"
          >
            无效输入 "{searchContent.slice(0, 50)}
            {searchContent.length > 50 ? "..." : ""}"
          </Alert>
        </Snackbar>
        <Image src={"/images/logo.png"} width={80} height={80} />
        <Toolbar sx={{ mt: 2, width: "100%", maxWidth: "1000px" }}>
          <SearchBar
            value={searchContent}
            handleChange={(event: {
              target: { value: React.SetStateAction<string> };
            }) => {
              setSearchContent(event.target.value);
              setOpen(false);
            }}
            handleSearch={() => {
              const result = parseSearchContent();
              if (!result) {
                setOpen(true);
              }
            }}
            handleClear={() => setSearchContent("")}
          />
        </Toolbar>
      </Box>
    </>
  );
}

export default Home;
