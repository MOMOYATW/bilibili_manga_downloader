import { createTheme } from "@mui/material/styles";

// Create a theme instance.
export const lightTheme = createTheme({
  typography: {
    fontFamily: ["Work Sans", "Noto Sans SC"].join(","),
  },
  palette: {
    secondary: { main: "#1976d2" },
    warning: { main: "#1976d2" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "transparent",
            width: "0.5rem",
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 8,
            backgroundColor: "#e0e0e0",
            minHeight: 24,
          },
          "&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active":
            {
              backgroundColor: "#d4d4d4",
            },
          "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover":
            {
              backgroundColor: "#d4d4d4",
            },
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  typography: {
    fontFamily: ["Work Sans", "Noto Sans SC"].join(","),
  },
  palette: {
    mode: "dark",
    background: { default: "#1e1e1e", paper: "#1e1e1e" },
    secondary: { main: "#2c2a38" },
    warning: { main: "#2c2a38" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "transparent",
            width: "0.5rem",
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 8,
            backgroundColor: "#424242",
            minHeight: 24,
          },
          "&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active":
            {
              backgroundColor: "#4f4f4f",
            },
          "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover":
            {
              backgroundColor: "#4f4f4f",
            },
        },
      },
    },
  },
});

export const onimaiTheme = createTheme({
  typography: {
    fontFamily: ["Work Sans", "Noto Sans SC"].join(","),
  },
  palette: {
    primary: { main: "#faf8c9", contrastText: "#936454" },
    secondary: { main: "#62b6d8", contrastText: "#fff" },
    warning: { main: "#ee858c", contrastText: "#fff" },
    info: { main: "#f2dcd6" },
    text: { primary: "#936454" },
    background: { default: "#faf8c9", paper: "#faf8c9" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "transparent",
            width: "0.5rem",
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 8,
            backgroundColor: "#e0e0e0",
            minHeight: 24,
          },
          "&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active":
            {
              backgroundColor: "#d4d4d4",
            },
          "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover":
            {
              backgroundColor: "#d4d4d4",
            },
        },
      },
    },
  },
});

export const theme = {
  default: { light: lightTheme, dark: darkTheme },
  onimai: { light: onimaiTheme, dark: darkTheme },
};
