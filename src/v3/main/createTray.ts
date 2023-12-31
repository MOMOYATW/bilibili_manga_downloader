import { Menu, Tray } from "electron";
import path from "path";

export function createTray(
  onShowWindow: Function,
  onCloseWindow: Function
) {
  const isProd: boolean = process.env.NODE_ENV === "production";
  const tray = new Tray(
    isProd
      ? path.join(process.resourcesPath, "static", "icon-64.png")
      : path.join("static", "icon-64.png")
  );
  tray.setToolTip("Bilibili Manga Downloader");
  tray.on("click", () => {
    onShowWindow();
  });
  const contextMenu = Menu.buildFromTemplate([
    {
      label: "显示窗口",
      click: () => {
        onShowWindow();
      },
    },
    {
      // divider
      type: "separator",
    },
    {
      label: "退出",
      click: () => {
        onCloseWindow();
      },
    },
  ]);
  tray.setContextMenu(contextMenu);
}
