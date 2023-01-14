import {
  Box,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  useTheme,
} from "@mui/material";
import Link from "./Link";
import styles from "../styles/LeftNavBar.module.css";

const drawerWidth = 160;

const LeftNavBar = ({ activeMenuIndex, onClickMenuBtn, menuItems }) => {
  const theme = useTheme();
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: "border-box" },
      }}
      PaperProps={{
        sx: {
          backgroundColor: theme.palette.background.default,
        },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: "auto" }}>
        <List className={styles.list}>
          {menuItems.map((item, index: number) => {
            if (item === undefined) return <Divider key={"divider"} />;
            return (
              <ListItem key={item.title} disablePadding>
                <ListItemButton
                  selected={activeMenuIndex === index}
                  onClick={() => onClickMenuBtn(index)}
                  sx={{
                    p: 0,
                    "&.Mui-selected": {
                      backgroundColor:
                        index % 2
                          ? theme.palette.secondary.main
                          : theme.palette.warning.main,
                      color: theme.palette.secondary.contrastText,
                    },
                    "&.Mui-selected:hover": {
                      backgroundColor:
                        index % 2
                          ? theme.palette.secondary.dark
                          : theme.palette.warning.dark,
                      color: theme.palette.secondary.contrastText,
                    },
                  }}
                >
                  <Link href={item.href} naked>
                    <ListItemText
                      primary={item.title}
                      disableTypography
                      sx={{ fontSize: "0.9rem" }}
                    />
                  </Link>
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>
    </Drawer>
  );
};

export default LeftNavBar;
