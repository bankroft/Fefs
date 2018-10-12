## 软件下载

- 下载[`erya-*-pyinstaller-F.zip`](https://github.com/bankroft/chaoxing-MOOC-beta/releases)
- 下载[`erya-console.zip`](https://github.com/bankroft/erya-console/archive/1.0.zip)

解压文件

## 使用方法：

### exe运行
0. 安装`chrome` 版本`v68-70`
0. 修改`raccount.txt`文件，内容为若快平台账号和密码，格式为username|password
1. 配置`config.ini`[内容](#config.ini注释)(文件内有各项注释)
2. 运行`rest_console.exe`文件
3. 打开release下载的`erya console`文件，运行`index.html`

### 源码运行(python)

#### python >= 3.6

0. 安装必要库`pip install -r requirements.txt`
1. 运行`python rest_console.py`

## 版本更新记录

[我的博客](https://www.bankroft.cn/?p=37, "my blog")

## 交流反馈群

![二维码](https://i.loli.net/2018/10/08/5bbb1cb62dc66.png)

### config.ini注释

```ini
[Server]
;配置rest监听地址,非必要无需改变
ip=127.0.0.1
port=27088

[queryHTTP]
;配置HTTP查询
url_query=http://erya.bankroft.cn/api/query
url_update=http://erya.bankroft.cn/api/update

[queryMethod]
;1表示直接连接数据库读取，2表示通过http获取
m=2

[program]
debug=False

[wechat]
; 查题公众号
wechat = 

[User]
;是否观看，待定
watch_video=True
test_question=True
; 未查到答案等待时间，单位分钟
noanswer_sleep = 5
; 自动切换播放线路
internet_line = 公网1
```

## Contributor
感谢[@ningyuv](https://github.com/ningyuv '2018-10-5')为本项目提供的视频内答题统一解决办法