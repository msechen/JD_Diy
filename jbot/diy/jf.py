#diybot插件文件，放置于diy文件夹
#使用方法：私有bot对话内发送/jf+商品链接，支持单个或者多个链接
from email import message
from telethon import events
from .. import jdbot, chat_id, JD_DIR, BOT_SET, ch_name
from urllib import parse
import requests, time, os, json, sys, re, random
from .utils import read, write
import asyncio



# 返利
@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/jf'))
async def rebate_sku(event):
    messages = event.message.text.split("/jf ")[1].split('\n')
    messages = filter(None, messages)
    key="jf_convert_url"
    strReturn=""
    home=""
    imgurl=""
    for message in messages:
        if "u.jd.com" in message:
            try:
                kv=f'{key}="{message}"'
                change=""
                configs = read("str")
                if kv not in configs:
                    if key in configs:
                        configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                        change += f"【替换】环境变量:`{kv}`\n"  
                        write(configs)
                    else:
                        configs = read("str")
                        configs += f'export {key}="{message}"\n'
                        change += f"【新增】环境变量:`{kv}`\n"  
                        write(configs)
                if os.path.exists("/ql/scripts/jf.js"):
                    cmdtext="task /ql/scripts/jf.js now"
                elif os.path.exists("/jd/scripts/jf.js"):
                    cmdtext="jtask /jd/scripts/jf.js now"
                p = await asyncio.create_subprocess_shell(cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                res_bytes, res_err = await p.communicate()
                res = res_bytes.decode('utf-8') 
                txt=res.split('\n')
                if res:
                    for line in txt:
                        if "imgurl" in line:
                            imgurl =line.split('：')[1]
                        if "🏠" in line:
                            home =line
                        if "💰" in line or "🚗" in line or "🐲" in line:
                            strReturn += line +'\n'
            except Exception as e:
                print(e)
    if strReturn:
        await jdbot.send_message(chat_id, strReturn+'\n'+home, file=imgurl)
    else:
        await jdbot.send_message(chat_id,'查询失败!')


if ch_name:
    jdbot.add_event_handler(
        rebate_sku,
        events.NewMessage(chats=chat_id, pattern=BOT_SET['命令别名']['jf']))