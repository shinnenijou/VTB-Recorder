# VTB-Recorder
 
自用VTB录像机, 目前支持平台: Twitcasting, bilibili
TODO: 加入Youtube录制

# 依赖
0. 网络请求使用`requests`, pip安装即可

1. 录像部分依赖`Streamlink`, 可以通过`apt`, `yum`, `pip`等工具下载。注意版本要求>=2.1.0
否则将无法录制Twitcasting带密码的直播. 详细指引见[Streamlink_Docs](https://streamlink.github.io/install.html)

2. 转码部分依赖`ffmpeg`, 下载对应平台已编译的二进制文件即可, 可选镜像[ffmpeg镜像](https://johnvansickle.com/ffmpeg/)
下载并解压后将ffmpeg移动到`/usr/local/bin`中

3. 上传部分依赖`rclone`, 下载对应平台已编译的二进制文件即可, 见[RCLONE](https://rclone.org/downloads/)
下载后需要完成drive账号的配置，详细步骤说明在[RCLONE](https://rclone.org/overview/)查阅网盘供应商对应的说明