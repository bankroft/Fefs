## 软件下载

#### 链接1

- [`erya-*-pyinstaller-F.zip`](https://github.com/bankroft/chaoxing-MOOC-beta/releases)

#### 链接2

- OneDrive[`chaoxing tools`](https://1drv.ms/f/s!Avzz1Vbw4dVFkIZID8yjlW684QWL2g)

**解压文件**

## 使用方法：

### exe运行
1. 安装`chrome` 版本`v68-70`
2. 运行`rest_console.exe`文件(如果设置了微信公众号，弹出图片请使用微信扫描)
3. 建议首先选择`设置`功能

### 源码运行(python)

#### python >= 3.6

1. 安装必要库`pip install -r requirements.txt`
2. 运行`python rest_console.py`

## 版本更新记录

[我的博客](https://www.bankroft.cn/?p=37, "my blog")

## 交流反馈群(新版打包会先发到群里)

![二维码](https://i.loli.net/2018/10/08/5bbb1cb62dc66.png)

### config.ini注释

```ini
[queryHTTP]
;HTTP查题api
url_query=http://erya.bankroft.cn/api/query
url_update=http://erya.bankroft.cn/api/update

[User]
; 微信查题公众号
wechat_mp =
; 未查到答案等待时间，单位分钟
noanswer_sleep = 5
; 自动切换播放线路
internet_line = 公网1
```

## Contributor
感谢[@ningyuv](https://github.com/ningyuv '2018-10-5')为本项目提供的视频内答题统一解决办法