## 使用方法：
0. 修改raccount.txt文件，内容为若快平台账号和密码，格式为username|password
1. 配置config.ini,文件内有各项说明
2. 命令行运行rest_console.exe文件
3. 打开release下载的erya console文件，运行index.html：

-------------------

具体使用方法[我的博客](https://www.bankroft.cn/?p=37, "my blog")

------------------

### config.ini说明
```ini
[Server]
;配置rest监听地址,非必要无需改变
ip=127.0.0.1
port=27088

[queryHTTP]
;配置HTTP查询
url_query=http://erya.bankroft.cn/query
url_update=http://erya.bankroft.cn/update

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