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
      <Box display="flex" width={"50%"}>
        <Image src={"/images/404.png"} height={1000} width={1000} />
      </Box>
      <Typography
        variant="h3"
        component="div"
        fontWeight={"bold"}
        sx={{ mt: 2 }}
      >
        你是怎么办到的！？
      </Typography>
    </Box>
  );
};

export default Error404;
