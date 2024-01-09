# 基于现代 GUI 的哔哩哔哩漫画下载器

<div align="center">
<img src="README.assets/icon.png" width=100px>
</div>
<div align="center" padding="1">
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest"><img src="https://img.shields.io/github/release/MOMOYATW/bilibili_manga_downloader.svg?logo=github" alt="GitHub release"></a> 
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest"><img src="https://img.shields.io/badge/platform-Windows_|_Linux-blue?logo=github" alt="Support platform"></a> 
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/stargazers"><img src="https://img.shields.io/github/stars/MOMOYATW/bilibili_manga_downloader.svg?logo=github" alt="Github stars"></a>
</div>
<div align="center" padding="1">
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader?tab=MIT-1-ov-file"><img src="https://img.shields.io/github/license/MOMOYATW/bilibili_manga_downloader?logo=github" alt="License"></a> 
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest"><img src="https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/latest/total.svg?logo=github" alt="GitHub downloads"></a>
<a href="https://github.com/MOMOYATW/bilibili_manga_downloader/releases/latest"><img src="https://img.shields.io/github/downloads/MOMOYATW/bilibili_manga_downloader/total.svg?logo=github" alt="GitHub downloads"></a> 


</div>


## 3.0 全新架构

<div align="center">

## 新版特性

下载速度快！

交互界面好！

体积有减少！

</div>

### 软件界面

<img src="README.assets/image-20230112221530823.png" width="700px">

### 使用说明

在栏中填入漫画网址进行搜索，即可获取漫画信息，也支持直接搜索关键词

目前支持漫画详细页面网址，形如`https://manga.bilibili.com/detail/mc28528?from=manga_person`

漫画单话网址，形如 `https://manga.bilibili.com/mc26731/329893?from=manga_detail`

关键词，形如`关于前辈很烦人`

<img src="README.assets/image-20230118171740926.png" width="700px">

<img src="README.assets/image-20230112221828757.png" width="700px">

选中可以下载的漫画，点击开始下载即可添加到下载列表中

<img src="README.assets/image-20230112221949394.png" width="700px">

<img src="README.assets/image-20230115125351648.png" width="700px">

<img src="README.assets/image-20230115125316936.png" width="700px">

对于有**特典**的漫画，其特典信息将被追加到列表的末尾，请留意。

<img src="README.assets/image-20230112222204760.png" width="700px">

> #### 关于特典
>
> 按照官方介绍，目前特典有三种形式：视频、动图、图片。目前已经对视频和图片都进行了支持，但是动图由于暂时还没有遇到，因此也无法测试。
>
> 我推测动图就是没有声音的视频，因此理论上当前版本也可以下载。不过如果有人遇到了问题欢迎在 issue 中提出。

下载过程中可以单击任务，从而打开详情窗口。

<img src="README.assets/image-20230115125512120.png" width="700px">

由于 B 站下载图片不支持断点续传，因此没有设计暂停功能，可以在下载过程中取消下载。

下载记录将会在程序正常关闭时保存到文件中。

有关设置，新版本设置项变为以下几项

<img src="README.assets/image-20230115125750982.png" width="700px">

<img src="README.assets/image-20230115125818344.png" width="700px">

Token：用户登录后的`SESSDATA`项 Cookie 值，现支持直接自动获取。点击获取 Token 按钮，在打开的窗口中登录 b 站账号，完成后关闭即可。需要注意的是，在程序内登录后 Cookie 会更新，这会导致网页端的账号被登出。该值亦可手动设置，详细步骤见下文。

下载路径：选择图片存储位置。

漫画文件夹名称格式：

- `{title}` 表示漫画标题
- `{id}`表示漫画 ID
- `{authors}`表示作者

每话文件夹名称格式：

- `{title}` 表示每集标题
- `{short_title}` 表示每集短标题
- `{id}` 表示每集 ID
- `{index}` 表示每集序号

同时下载集数控制下载速度，默认为 1.

==下载完成后是否压缩==，该选项开启后会在每集下载完成后对该漫画文件夹进行压缩，随着该漫画文件夹所含有的话数越来越多，压缩速度也会逐渐变慢。因此推荐在需要下载任务的全部完成后手动进行压缩。

新版本开代理时也可以使用，无需手动设置。

> #### 有关于登录 cookie 的获取
>
> 在网页上登录后，对于 edge 浏览器，进行如下操作
>
> <img src="README.assets/image-20230113175759365.png" width="500px">
>
> <img src="README.assets/image-20230113175843643.png" width="500px">
>
> <img src="README.assets/image-20230113175941465.png" width="500px">
>
> 将得到的 SESSDATA 值直接以`你的SESSDATA值`的形式填入设置中即可
>
> 请注意该值切不可泄露

目前程序自动检查更新，检查到新版本时会自动在后台下载，下载完成后弹出提示告知用户退出程序时将进行新版本安装。

继承前一个版本，新版本也有亮色和暗色两个主题，点击即可切换。

<img src="README.assets/image-20230112223958612.png" width="700px">

### 自行编译与运行

配置依赖
```
$ cd src/v3

# using yarn or npm
$ yarn (or `npm install`)
```

调试模式运行
```
$ yarn dev (or `npm run dev`)
```

编译
```
$ yarn build (or `npm run build`)
```

注意：MacOS用户请查询electron-builder配置`electron-builder.yml`文件

### 项目基于

- Electron
- Material UI
- Next.js
---
### 免责声明

1. 本项目（以下简称“软件”）仅供学习和研究之用，不鼓励或支持侵犯版权、违反法律或违反任何网站的使用政策。

2. 使用本软件的用户应自行承担风险。作者不对使用本软件导致的任何损失、法律纠纷或其他后果负责。

3. 本软件可能会对目标网站的服务器造成一定的负载，使用者应当谨慎使用，以避免对目标网站造成不必要的干扰或损害。

4. 本软件按“原样”提供，作者不提供任何明示或暗示的保证，包括但不限于适销性、特定用途适用性、无侵权性等方面的保证。

5. 作者不对用户使用本软件的行为负责，包括但不限于用户违反法律或任何第三方权益的行为。

6. 使用本软件即表示您同意遵守本免责声明和任何适用的法律法规。

作者保留对本免责声明进行修改和更新的权利，敬请查看最新版本。

---

### 更新

V3.2.2

1. 增加对Linux平台的支持，修复了在Linux下的一些适配性问题（issue #25）
2. 发布Linux二进制版本，在ubuntu 20.04上通过测试
3. 明确了各发行版本所支持架构，其他架构请对照README自行编译
4. 修复了上个版本中关于界面图标不显示的问题
   

### 开发计划
