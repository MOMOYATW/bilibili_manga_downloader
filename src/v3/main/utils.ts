import fs from "fs";
import {
  ComicDetailData,
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";
import path from "path";
import child_process from "child_process";

export function readJSONasObject<T>(jsonFileName: string, defaultObject: T): T {
  if (fs.existsSync(jsonFileName)) {
    const objectRead = JSON.parse(fs.readFileSync(jsonFileName, "utf-8"));
    return objectRead;
  }
  return defaultObject;
}

export function writeObjectasJSON<T>(jsonFileName: string, writeObject: T) {
  // get the directory of the json file
  const writeDirectory = path.dirname(jsonFileName);
  if (!fs.existsSync(writeDirectory)) fs.mkdirSync(writeDirectory);
  fs.writeFileSync(jsonFileName, JSON.stringify(writeObject, null, 2), "utf-8");
}

export function slugify(str: string): string {
  return str
    .replace(/[\\\/\:\*\?\"\<\>\|]/g, "")
    .replace(/\.*$/g, "")
    .trim();
}
const isProd: boolean = process.env.NODE_ENV === "production";
export function zipDirectory(
  sourceDir: string,
  outPath: string,
  callback_function: Function
) {
  sourceDir = path.join(sourceDir, "*");
  console.log(sourceDir, outPath);
  // judge platform
  let path_7z = "";
  if (process.platform === "win32") {
    path_7z = isProd
      ? path.join(process.resourcesPath, "static", "7zr.exe")
      : path.join("static", "7zr.exe");
  }
  else if (process.platform === "linux") {
    path_7z = isProd
      ? path.join(process.resourcesPath, "static", "7zzs")
      : path.join("static", "7zzs");
  }
  else {
    console.log("Not Implemented Yet.")
    return;
  }
  let child: child_process.ChildProcessWithoutNullStreams;

  if (!fs.existsSync(outPath)) {
    child = child_process.spawn(path_7z, ["a", outPath, sourceDir]);
  } else {
    child = child_process.spawn(path_7z, ["u", outPath, sourceDir]);
  }
  child.on("exit", () => {
    callback_function();
  });
  child.on("error", (error) => console.log(error));
}

export function generateComicPath(format: string, comicInfo: ComicDetailData) {
  return format
    .replaceAll("{title}", comicInfo.title)
    .replaceAll("{id}", comicInfo.id.toString())
    .replaceAll("{authors}", comicInfo.author_name.toString())
    .replaceAll(/\{.*\}/g, "");
}

export function generateEpisodePath(
  format: string,
  episodeInfo: ComicEpisodeObject
) {
  return format
    .replaceAll("{title}", episodeInfo.title)
    .replaceAll("{short_title}", episodeInfo.short_title)
    .replaceAll("{id}", episodeInfo.id.toString())
    .replaceAll("{index}", episodeInfo.ord.toString())
    .replaceAll(/\{.*\}/g, "");
}

export function generateImageName(format: string, index: number) {
  return format
    .replaceAll("{index}", index.toString().padStart(3, "0"))
    .replaceAll(/\{.*\}/g, "");
}

export function generateTokutenPath(
  format: string,
  tokutenInfo: ComicPlusItemObject
) {
  return format
    .replaceAll("{title}", tokutenInfo.title)
    .replaceAll("{detail}", tokutenInfo.detail)
    .replaceAll("{id}", tokutenInfo.id.toString())
    .replaceAll(/\{.*\}/g, "");
}

export function generateMetadata(
  metadata_type = "tachiyomi",
  comicInfo: ComicDetailData,
  download_path: string,
  comic_folder_format: string
) {
  const comicFolderName = generateComicPath(comic_folder_format, comicInfo);
  switch (metadata_type) {
    case "tachiyomi":
      const meta_data = {
        title: comicInfo.title,
        author: comicInfo.author_name.toString(),
        artist: comicInfo.author_name.toString(),
        description: comicInfo.classic_lines,
        genre: comicInfo.tags
          .map((tag) => tag.name)
          .concat(comicInfo.styles2.map((tag) => tag.name)),
        status: comicInfo.is_finish ? 2 : 1,
      };
      console.log("save json");
      writeObjectasJSON(
        path.join(download_path, slugify(comicFolderName), "detail.json"),
        meta_data
      );
      break;
  }
}
