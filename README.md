# 基于现代 GUI 的哔哩哔哩漫画下载器

[![GitHub release](https://img.shields.io/github/release/MOMOYATW/bilibili_manga_downloader.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/latest/total.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/total.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases)

## 2.0 版本大升级

### 软件界面

![](README_imgs/2022-06-04-19-01-12.png =500x)

### 使用说明

在栏中填入漫画网址进行搜索，即可获取漫画信息
目前仅支持漫画详细页面网址，形如`https://manga.bilibili.com/detail/mc28528?from=manga_person`
未来计划追加支持根据某话网址进行下载以及关键词搜索

![](README_imgs/2022-06-04-19-04-16.png =500x)

选中可以下载的漫画，点击开始下载即可添加到下载列表中
![](README_imgs/2022-06-04-19-05-13.png =500x)
![](README_imgs/2022-06-04-19-05-38.png =500x)
![](README_imgs/2022-06-04-19-05-44.png =500x)

对于有**特典**的漫画，其特典信息将被追加到列表的末尾，请留意。
![](README_imgs/2022-06-04-19-14-00.png =500x)

在设置中，可以将登陆后的 cookie 粘贴到此处，从而下载付费漫画，另外可以修改下载图片宽度，默认下载路径，下载最大线程数，是否启动时检查更新以及每张图片的请求间隔。
![](README_imgs/2022-06-04-19-06-46.png =500x)

注意：多线程下载容易导致请求过于频繁，进而导致下载失败，因此谨慎选择。

### 项目依赖包

- requests
- pyside6

---

### 更新

#### V2.0.0

1. 重新设计了界面，并对代码进行了重写
2. 增加版本号检查功能
3. 增加了特典下载功能
