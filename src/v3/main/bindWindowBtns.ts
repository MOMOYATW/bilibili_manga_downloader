export function bindWindowBtns(
  ipcMain: Electron.IpcMain,
  mainWindow: Electron.CrossProcessExports.BrowserWindow
) {
  //Minimise the app
  ipcMain.on("minimiseApp", () => {
    console.log("Clicked Minimise button!");
    mainWindow.minimize();
  });

  // Maximize Restore App
  ipcMain.on("maximizeRestoreApp", () => {
    if (mainWindow.isMaximized()) {
      mainWindow.restore();
    } else {
      mainWindow.maximize();
    }
  });

  //Check if maximized
  mainWindow.on("maximize", () => {
    mainWindow.webContents.send("isMaximized");
  });

  // Check if is restored
  mainWindow.on("unmaximize", () => {
    mainWindow.webContents.send("isRestored");
  });
}
