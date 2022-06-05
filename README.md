# 基于现代 GUI 的哔哩哔哩漫画下载器

[![GitHub release](https://img.shields.io/github/release/MOMOYATW/bilibili_manga_downloader.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/latest/total.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/total.svg?logo=github)](https://github.com/MOMOYATW/bilibili_manga_downloader/releases)

## 2.0 版本大升级

### 软件界面

<img src="README_imgs/2022-06-04-19-01-12.png" width="500px">

### 使用说明

在栏中填入漫画网址进行搜索，即可获取漫画信息
目前仅支持漫画详细页面网址，形如`https://manga.bilibili.com/detail/mc28528?from=manga_person`
未来计划追加支持根据某话网址进行下载以及关键词搜索

<img src="README_imgs/2022-06-04-19-04-16.png" width="500px">

选中可以下载的漫画，点击开始下载即可添加到下载列表中
<img src="README_imgs/2022-06-04-19-05-13.png" width="500px">
<img src="README_imgs/2022-06-04-19-05-38.png" width="500px">
<img src="README_imgs/2022-06-04-19-05-44.png" width="500px">

对于有**特典**的漫画，其特典信息将被追加到列表的末尾，请留意。
<img src="README_imgs/2022-06-04-19-14-00.png" width="500px">

在设置中，可以将登陆后的 cookie 粘贴到此处，从而下载付费漫画，另外可以修改下载图片宽度，默认下载路径，下载最大线程数，是否启动时检查更新以及每张图片的请求间隔。
<img src="README_imgs/2022-06-04-19-06-46.png" width="500px">

> 有关于登录 cookie 的获取
> 在网页上登录后，对于 edge 浏览器，进行如下操作
> ![](README_imgs/2022-06-04-19-41-46.png) > ![](README_imgs/2022-06-04-19-42-22.png) > ![](README_imgs/2022-06-04-19-44-12.png)
>
> 将得到的 SESSDATA 值以`{"SESSDATA":"你的SESSDATA值"}`的形式填入设置中即可
> 请注意该值切不可泄露

注意：多线程下载容易导致请求过于频繁，进而导致下载失败，因此谨慎选择。

### 项目依赖包

- requests
- pyside6

---

### 更新

#### V2.1.0

1. 追加了对特典视频的支持
2. 支持断点续传
3. 修改了选择文件夹的逻辑，如需使用相对路径请手动输入
4. 增加对不同格式的图像支持
5. 优化了进度条更新逻辑
