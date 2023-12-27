import { Box, CircularProgress } from "@mui/material";

const Loading = () => {
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
      <CircularProgress color="inherit" sx={{ mb: 1 }} />
      加载中...
    </Box>
  );
};

export default Loading;
