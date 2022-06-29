#适配diybot，存放diy文件夹，回复一个商品链接jf
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio, datetime, os, re, sys, time, json, requests, random
from unittest import result
from telethon import events
from urllib import parse
from .user import client
from .. import chat_id, jdbot, logger, API_ID, API_HASH, PROXY_START, proxy, JD_DIR, TOKEN
from .utils import read, write


# 返利
@client.on(events.NewMessage(pattern=r'^jf$', outgoing=True))
async def jf(event):
    reply = await event.get_reply_message()
    messages = event.message.text.split("\n")
    if event.is_reply:
        messages = reply.text.split("\n")
    messages = filter(None, messages)
    key="jf_convert_url"
    strReturn=""
    home=""
    imgurl=""
    for message1 in messages:
        if "u.jd.com" in message1:
            message = re.findall(r'((?:https://|http://)u.jd.com/[A-Za-z0-9]+)', message1)[0]
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
                        if "🏠" in line:
                            home =line
                        if "💰" in line or "🚗" in line or "🐲" in line:
                            strReturn += line +'\n'
            except Exception as e:
                print(e)
    if strReturn:
        await event.edit(strReturn+'\n'+home)
    else:
        await event.edit('查询失败!')
