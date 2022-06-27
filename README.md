<h1 align="center">
  diy机器人
  <br>
  Author: chiupam
</h1>

## 目录
- [目录](#目录)
- [仓库目录说明](#仓库目录说明)
- [版权](#版权)
- [声明](#声明)
- [特别感谢](#特别感谢)
- [简介](#简介)
- [已有功能](#已有功能)
  - [基础功能](#基础功能)
  - [user功能](#user功能)
  - [整合人形bot](#整合人形bot)
- [使用方式](#使用方式)
  - [部署机器人](#部署机器人)
  - [开启user监控机器人](#开启user监控机器人)
- [前瞻计划](#前瞻计划)
  - [用户要求](#用户要求)
  - [部署方法](#部署方法)
- [已知问题](#已知问题)
# 仓库目录说明
```text
JD_Diy/                     # JD_Diy 仓库
  |-- backup                    # 移除的旧文件
  |-- beta                      # 测试版机器人
  |-- config                    # 配置目录
  |-- jbot                      # 正式版机器人
  |-- module                    # 实例模块
  |-- other                     # 不便于分类脚本
  |-- pys                       # python脚本
  |-- shell                     # shell脚本
  |-- requirements.txt          # 依赖文件
  `-- README.md                 # 仓库说明
```
# 版权
- 未经本人同意，仓库内所有资源文件，禁止任何公众号、自媒体、开发者进行任何形式的转载、发布、搬运。
# 声明
- 这不是一个开源项目，只是把 GitHub 当作一个代码的存储空间，本项目不接受任何开源要求。
- 仅用于学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
- 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。
- 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本人对于由此引起的任何隐私泄漏或其他后果概不负责。
- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明、所有权证明，我将在收到认证文件后删除相关脚本。
- 任何以任何方式查看此项目的人或者以直接或间接的方式使用该项目的任何脚本的使用者都应仔细阅读此声明。 本人保留随时更改或补充此免责声明的权利。一旦使用并复制或使用了任何相关脚本，则视为您已接受此免责声明。
- 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。
# 特别感谢
- 脚本的写作参考了 [SuMaiKaDe](https://github.com/SuMaiKaDe) 的 [bot](https://github.com/SuMaiKaDe/bot) 仓库
- 模块的写作参考了 lxk0301 的 jd_scripts 仓库
## 简介
随着 v4-bot 启动而启动的机器人，其中大部分功能亦支持青龙用户。
## 已有功能
### 基础功能
- [x] 发送 `/start` 指令查看机器人说明
- [x] 发送 `/restart` 指令可重启机器人
- [x] 发送 `/help` 指令可获取快捷命令
- [x] 发送 `/upbot` 升级机器人
- [x] 发送 `/checkcookie` 检测过期情况
- [x] 发送 `/export` 修改环境变量
- [x] 发送 `/blockcookie` 进行屏蔽操作
- [x] 发送 `pin=xxx;wskey=xxx;` 快速添加 `wskey`
- [x] 发送链接直接下载 `.js` `.sh` 的 `raw` 文件
- [x] 添加以 `.git` 结尾的仓库链接可添加仓库
- [x] 发送 `变量名="变量值"` 的格式消息可快捷添加环境变量
### user功能
- [x] 发送 `/user` 开启或管理user监控
- [x] 关注店铺有礼自动执行（需自行配置频道ID）
- [x] 自动替换某些环境变量（需自行配置频道ID）
- [x] 监控群组聊天记录（仅文字）
- [ ] 自动参加抽奖机器人发送的抽奖活动
- [ ] 自动下载频道/某人的特定文件
### 整合人形bot
- [x] re
- [x] id
- [x] del
- [x] da
- [ ] weather
- [ ] ...
# 使用方法
## 部署机器人
进入容器中执行以下命令即可
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi
mkdir $root/repo/backup/$(date +\%Y\%m\%d)
cp -rf $root/jbot/* $root/repo/backup/$(date +\%Y\%m\%d)
rm -rf $root/jbot/*
wget https://raw.githubusercontent.com/msechen/JD_Diy/main/shell/bot.sh -O $root/bot.sh
bash $root/bot.sh
```
## 开启user监控机器人
```text
在部署机器人成功后使用 /codelogin 指令，选择重新登录即可。
但是不要在短时内登陆过多次数，因为会报以下错误。
A wait of **** seconds is required.（需要等待 **** 秒。）
```
# 前瞻计划
测试版机器人的部署方法，功能不稳定，不建议尝试。
## 用户要求
- 比较热爱折腾
- 一定的操作基础
- 甚至可以 Pr 部分功能
## 部署方法
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi
mkdir $root/repo/backup/$(date +\%Y\%m\%d)
cp -rf $root/jbot/* $root/repo/backup/$(date +\%Y\%m\%d)
rm -rf $root/jbot/*
wget https://raw.githubusercontent.com/msechen/JD_Diy/main/shell/bot_beta.sh -O $root/bot.sh
bash $root/bot.sh
```
# 已知问题
1. 重装机器人后 `/start` 没有反应
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi
rm -f $root/bot.session
rm -f $root/bot.session-journal
rm -f $root/user.session
rm -f $root/user.session-journal
rm -f $root/config/user.session
rm -f $root/config/user.session-journal
sed -i 's/user": "True"/user": "False"/' $root/config/botset.json
if [ -d "/ql" ]; then
  ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
  nohup python3 -m jbot > $root/log/bot/bot.log 2>&1 &
else
  cd $root/jbot; pm2 start ecosystem.config.js
  cd $root; pm2 restart jbot
fi
```
2. `/user` 点击 `开启user` 按钮后连 `/start` 都没有反应
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi
rm -f $root/user.session
rm -f $root/user.session-journal
rm -f $root/config/user.session
rm -f $root/config/user.session-journal
sed -i 's/user": "True"/user": "False"/' $root/config/botset.json
if [ -d "/ql" ]; then
  ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
  nohup python3 -m jbot > $root/log/bot/bot.log 2>&1 &
else
  cd $root/jbot; pm2 start ecosystem.config.js
  cd $root; pm2 restart jbot
fi
```
3. 想用回之前自己最后一次备份好的机器人文件（可能无法使用user监控）
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi
if [ -d $root/repo/backup ]; then 
  echo "无法恢复user的正常监控！请悉知！"
  cd $root/repo/backup
  dir=$(ls -t | head -1 | awk '{print $1}')
  rm -rf $root/jbot/*
  cp -rf $root/repo/backup/$dir/* $root/jbot
  if [ -d "/ql" ]; then
    ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
    nohup python3 -m jbot > $root/log/bot/bot.log 2>&1 &
  else
    cd $root/jbot; pm2 start ecosystem.config.js
    cd $root; pm2 restart jbot
  fi
else 
  echo "你没有做备份！无法回滚！"
fi
```
