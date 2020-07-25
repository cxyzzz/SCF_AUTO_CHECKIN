# SCF_AUTO_CHECKIN

使用 SCF 自动完成 v2ex，吾爱破解论题，网易云音乐双端，天翼云签到

## 使用方法

1. 下载仓库中zip压缩包，运行环境选 python 3.6 空白模板，函数入口改为 `index.main` 上传到压缩包到 SCF 云函数
2. 配置环境变量

``` json
   QY_WEIXING_BOT_KEY: xxxxxxx          # 企业微信应用推送 key，注册方面自行百度，如不使用需要注释掉 index.py 中所有 push(xxx)
   NETEASE_COOKIE: MUSIC_U=xxxxxxx      # 网易云音乐 cookie
   V2EX_COOKIE: 2|1:0|10:xxx|2:A2|56:xxxx|xxxxxxx  # v2ex A2 cookie
   YYETS_ACCOUNT: xxxx                  # 人人影视账号
   YYETS_PASSWORD: xxx                  # 人人影视密码
   C189_ACCOUNT: xxx                    # 天翼网盘账号
   C189_PASSWORD: xxx                   # 天翼网盘密码
```

3. 设置触发器

触发管理选择定时触发，设置每天几点执行即可
