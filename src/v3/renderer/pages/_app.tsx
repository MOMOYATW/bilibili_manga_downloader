import "../styles/global.css";
import React from "react";
import Head from "next/head";
import type { AppProps } from "next/app";
import { Box, CssBaseline, styled, ThemeProvider } from "@mui/material";
import { lightTheme, darkTheme } from "../lib/theme";
import type { EmotionCache } from "@emotion/cache";
import createEmotionCache from "../lib/create-emotion-cache";
import { CacheProvider } from "@emotion/react";
import { useEffect, useState } from "react";
import Header from "../components/Header";
import LeftNavBar from "../components/LeftNavBar";
import { useRouter } from "next/router";

const clientSideEmotionCache = createEmotionCache();

type MyAppProps = AppProps & {
  emotionCache?: EmotionCache;
};

function getActiveTheme(themeMode: "light" | "dark") {
  return themeMode === "light" ? lightTheme : darkTheme;
}

const ScrollBox = styled(Box, {
  shouldForwardProp: (prop) => prop !== "theme",
})(({ theme }) => ({
  flexGrow: 1,
  padding: 0,
  marginTop: "36px",
  height: `calc(100vh - ${theme.spacing(4.5)})`,
  overflow: "auto",
}));

export default function MyApp(props: MyAppProps) {
  const [activeTheme, setActiveTheme] = useState(lightTheme);
  const [selectedTheme, setSelectedTheme] = useState<"light" | "dark">("light");
  const [activeMenuIndex, setActiveMenuIndex] = useState(0);
  const [downloadList, setDownloadList] = useState({});
  const router = useRouter();
  const MenuList = [
    {
      title: "主页",
      href: "/home",
    },
    {
      title: "设置",
      href: "/settings",
    },
    {
      title: "关于",
      href: "/about",
    },
    undefined,
    {
      title: "队列中",
      href: "/pending",
    },
    {
      title: "下载中",
      href: "/downloading",
    },
    {
      title: "已完成",
      href: "/complete",
    },
  ];

  const toggleTheme: React.MouseEventHandler<HTMLAnchorElement> = () => {
    const desiredTheme = selectedTheme === "light" ? "dark" : "light";

    setSelectedTheme(desiredTheme);
  };

  useEffect(() => {
    setActiveTheme(getActiveTheme(selectedTheme));
  }, [selectedTheme]);

  useEffect(() => {
    setActiveMenuIndex(
      MenuList.findIndex((menu) => {
        if (menu === undefined) return false;
        return menu.href === router.pathname;
      })
    );
  }, [router.pathname]);

  const { Component, pageProps, emotionCache = clientSideEmotionCache } = props;

  return (
    <CacheProvider value={emotionCache}>
      <Head>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width"
        />
      </Head>
      <ThemeProvider theme={activeTheme}>
        <Box sx={{ display: "flex" }}>
          <CssBaseline />
          <Header toggleTheme={toggleTheme} theme={selectedTheme} />
          <LeftNavBar
            activeMenuIndex={activeMenuIndex}
            onClickMenuBtn={setActiveMenuIndex}
            menuItems={MenuList}
          />
          <ScrollBox component={"main"} className="enable-scroll">
            <Component
              {...pageProps}
              downloadList={downloadList}
              setDownloadList={setDownloadList}
            />
          </ScrollBox>
        </Box>
      </ThemeProvider>
    </CacheProvider>
  );
}
