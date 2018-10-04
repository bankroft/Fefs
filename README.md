## 软件下载

[下载地址](https://github.com/bankroft/chaoxing-MOOC-beta/releases)

#### *attention*
- 下载`erya-*-pyinstaller-F.zip`
- 下载`erya-console.zip`

解压文件

## 使用方法：
0. 安装`chrome` 版本`v68-70`
0. 修改`raccount.txt`文件，内容为若快平台账号和密码，格式为username|password
1. 配置`config.ini`[内容](#config.ini注释)(文件内有各项注释)
2. 运行`rest_console.exe`文件
3. 打开release下载的`erya console`文件，运行`index.html`

### 源码运行(python)

#### python >= 3.6

0. 安装必要库`pip install - requirements.txt`
1. 运行`python rest_console.py`

## 版本更新记录

[我的博客](https://www.bankroft.cn/?p=37, "my blog")

## 注意

现版本(0.63)仅支持视频内答题的`判断题`类型，作者没有待看的网络课账号，也无法调试。如果有谁愿意贡献账号让我调试更新，那么下个版本应该会支持其它类型(单选、多选等)
或者你中间遇到了其他类型题目，可以直接把账号给我专门添加这种类型，前提是   不要回答你遇到的题目


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