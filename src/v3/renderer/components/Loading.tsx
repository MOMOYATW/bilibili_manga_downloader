import { Alert, Box, Button, CircularProgress } from "@mui/material";
import { useRouter } from "next/router";
import React from "react";

const Loading = ({ failed }) => {
  const router = useRouter();
  return (
    <Box
      display="flex"
      flexDirection={"column"}
      sx={{
        p: 3,
        justifyContent: "center",
        height: "100%",
        alignItems: "center",
      }}
    >
      {!failed ? (
        <>
          <CircularProgress color="inherit" sx={{ mb: 1 }} />
          加载中...
        </>
      ) : (
        <Alert
          severity="error"
          action={
            <Button
              size={"small"}
              onClick={() =>
                router.push(
                  {
                    pathname: `/home`,
                  },
                  undefined,
                  { shallow: true }
                )
              }
            >
              返回主页
            </Button>
          }
        >
          解析失败
        </Alert>
      )}
    </Box>
  );
};

export default Loading;
