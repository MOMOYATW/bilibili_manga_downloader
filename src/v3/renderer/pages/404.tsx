import { Box, Typography } from "@mui/material";
import React from "react";
import Image from "next/image";
const Error404 = () => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={"column"}
      sx={{ height: "100%" }}
    >
      <Image src={"/images/404.svg"} height={400} width={400} />
      <Typography
        variant="h5"
        component="div"
        fontWeight={"bold"}
        sx={{ mt: 2 }}
      >
        未知的页面
      </Typography>
    </Box>
  );
};

export default Error404;
