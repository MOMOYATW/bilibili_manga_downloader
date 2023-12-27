import Image from "next/image";
import { Box, Typography } from "@mui/material";

const Error = () => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection={"column"}
      sx={{ height: "100%" }}
    >
      <Image src={"/images/error.svg"} width={400} height={400}></Image>
      <Typography variant="h5" sx={{ mt: 2 }} fontWeight={"bold"}>
        解析失败
      </Typography>
    </Box>
  );
};

export default Error;
