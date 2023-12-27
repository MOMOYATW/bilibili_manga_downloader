import {
  Box,
  CardMedia,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material";
import { ipcRenderer } from "electron";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Image from "next/image";
import { SearchResultObject } from "../../types";
import Loading from "../../components/Loading";

const SearchDetail = () => {
  const router = useRouter();
  const [searchResult, setSearchResult] = useState<SearchResultObject[] | null>(
    null
  );
  useEffect(() => {
    ipcRenderer.on("Search", (event, args: SearchResultObject[]) => {
      setSearchResult(args);
    });
    ipcRenderer.send("getSearch", router.query["keyword"]);
    return () => {
      ipcRenderer.removeAllListeners("Search");
    };
  }, []);
  return searchResult === null ? (
    <Loading />
  ) : (
    <Box
      display="flex"
      justifyContent="left"
      alignItems="top"
      flexDirection={"column"}
      sx={{ height: "100%", p: 3 }}
    >
      <Typography
        variant="h5"
        component="div"
        fontWeight={"bold"}
        sx={{ mt: 2, height: "90%" }}
      >
        {router.query["keyword"]} 的搜索结果
        {searchResult.length !== 0 ? (
          searchResult.map((resultItem) => {
            return (
              <ListItem key={resultItem.id} disablePadding>
                <ListItemButton
                  role={undefined}
                  onClick={() => {
                    router.push(`/comics/${resultItem.id}`);
                  }}
                >
                  <Box width={"250px"} sx={{ mr: 1 }}>
                    <CardMedia
                      component="img"
                      image={resultItem.horizontal_cover}
                      alt="Cover"
                    />
                  </Box>
                  <Box display={"flex"} flexDirection={"column"} width="100%">
                    <ListItemText
                      primary={
                        <span
                          dangerouslySetInnerHTML={{
                            __html: resultItem.title,
                          }}
                        ></span>
                      }
                      secondary={
                        <span
                          dangerouslySetInnerHTML={{
                            __html: resultItem.author_name.toString(),
                          }}
                        ></span>
                      }
                    />
                  </Box>
                </ListItemButton>
              </ListItem>
            );
          })
        ) : (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            flexDirection={"column"}
            sx={{ height: "100%" }}
          >
            <Image src={"/images/nothing.svg"} height={300} width={300} />
            <Typography variant="h6" component="div" sx={{ mt: 2 }}>
              没有搜索结果哟~
            </Typography>
          </Box>
        )}
      </Typography>
    </Box>
  );
};

export default SearchDetail;
