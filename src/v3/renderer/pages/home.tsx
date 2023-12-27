import { useEffect, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/router";
import { ipcRenderer } from "electron";
import { Box, Toolbar } from "@mui/material";
import SearchBar from "../components/SearchBar";
import PopoutAlert from "../components/PopoutAlert";

function Home() {
  const [searchContent, setSearchContent] = useState("");
  const [open, setOpen] = useState(false);
  const router = useRouter();

  const parseSearchContent = (searchContent: string) => {
    // check if is comic detail url
    const result_1 = searchContent.match(
      /manga\.bilibili\.com\/detail\/mc[0-9]*/
    );
    if (result_1 !== null) {
      const comicId = result_1[0].slice(28);
      router.push(`/comics/${comicId}`);
      return true;
    }
    // check if episode url
    const result_2 = searchContent.match(
      /manga\.bilibili\.com\/mc[0-9]*\/[0-9]*/
    );
    if (result_2 !== null) {
      const comicId = result_2[0].slice(21).split("/")[0];
      router.push(`/comics/${comicId}`);
      return true;
    }
    // search it
    const result_3 = searchContent.match(/^[^.\/?\\#%]+$/);
    if (result_3 !== null) {
      const searchContent = result_3[0].slice(0, 50);
      router.push(`/search/${searchContent}`);
      return true;
    }
    return false;
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={"column"}
      sx={{ height: "100%" }}
    >
      <PopoutAlert
        severity={"error"}
        open={open}
        handleClose={() => setOpen(false)}
      >
        无效输入 "{searchContent.slice(0, 50)}
        {searchContent.length > 50 ? "..." : ""}"
      </PopoutAlert>

      <Image src={"/images/logo.png"} width={80} height={80} />
      <Toolbar sx={{ mt: 2, width: "100%", maxWidth: "1000px" }}>
        <SearchBar
          value={searchContent}
          handleChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setSearchContent(event.target.value);
            setOpen(false);
          }}
          handleSearch={() => {
            const result = parseSearchContent(searchContent);
            if (!result) setOpen(true);
          }}
          handleClear={() => setSearchContent("")}
        />
      </Toolbar>
    </Box>
  );
}

export default Home;
