import fs from "fs";
import archiver from "archiver";
import {
  ComicDetailData,
  ComicEpisodeObject,
  ComicPlusItemObject,
} from "./bilibili-manga-client";

export function readJSONasObjectUpdate<T>(
  jsonFileName: string,
  defaultObject: T
): T {
  if (fs.existsSync(jsonFileName)) {
    const objectRead = JSON.parse(fs.readFileSync(jsonFileName, "utf-8"));
    Object.keys(defaultObject).map((key) => {
      if (objectRead[key]) {
        defaultObject[key] = objectRead[key];
      }
    });
  }
  return defaultObject;
}

export function readJSONasObject<T>(jsonFileName: string, defaultObject: T): T {
  if (fs.existsSync(jsonFileName)) {
    const objectRead = JSON.parse(fs.readFileSync(jsonFileName, "utf-8"));
    return objectRead;
  }
  return defaultObject;
}

export function writeObjectasJSON<T>(
  jsonFileName: string,
  writeObject: T,
  writeDirectory: string
) {
  if (!fs.existsSync(writeDirectory)) fs.mkdirSync(writeDirectory);
  fs.writeFileSync(jsonFileName, JSON.stringify(writeObject, null, 2), "utf-8");
}

export function slugify(str: string): string {
  return str.replace(/[^a-zA-Z0-9_\u3400-\u9FBF\s-\.]/g, "");
}

export function zipDirectory(
  sourceDir: string,
  outPath: string,
  callback_function: Function
) {
  console.log(sourceDir, outPath);
  const archive = archiver("zip", { zlib: { level: 9 } });
  const stream = fs.createWriteStream(outPath);
  archive
    .directory(sourceDir, false)
    .on("error", (err) => {
      console.log(err);
    })
    .pipe(stream);

  stream.on("close", () => {
    console.log("done");
    callback_function();
  });
  archive.finalize();
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
