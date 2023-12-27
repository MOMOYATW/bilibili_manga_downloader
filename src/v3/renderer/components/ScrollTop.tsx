import { Box, Fade, useScrollTrigger } from "@mui/material";

export function ScrollTop({ children, scrollTarget }) {
  const trigger = useScrollTrigger({
    target: scrollTarget ? scrollTarget : undefined,
    disableHysteresis: true,
    threshold: 100,
  });

  const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
    const anchor = (
      (event.target as HTMLDivElement).ownerDocument || document
    ).querySelector("#back-to-top-anchor");

    if (anchor) {
      anchor.scrollIntoView({
        block: "center",
      });
    }
  };

  return (
    <Fade in={trigger}>
      <Box
        onClick={handleClick}
        role="presentation"
        sx={{ position: "fixed", bottom: 40, right: 40 }}
      >
        {children}
      </Box>
    </Fade>
  );
}

export default ScrollTop;
