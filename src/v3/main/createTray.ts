import { Menu, Tray } from "electron";
import path from "path";

export function createTray(
  mainWindow: Electron.CrossProcessExports.BrowserWindow,
  beforequit_callback: Function
) {
  const isProd: boolean = process.env.NODE_ENV === "production";
  const tray = new Tray(
    isProd
      ? path.join(process.resourcesPath, "static", "icon-64.png")
      : path.join("static", "icon-64.png")
  );
  tray.setToolTip("Bilibili Manga Downloader");
  tray.on("click", () => {
    mainWindow.show();
  });
  const contextMenu = Menu.buildFromTemplate([
    {
      label: "显示窗口",
      click: () => {
        mainWindow.show();
      },
    },
    {
      // divider
      type: "separator",
    },
    {
      label: "退出",
      click: () => {
        beforequit_callback();
        mainWindow.close();
      },
    },
  ]);
  tray.setContextMenu(contextMenu);
}
