#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import requests
from requests import get, put, post
from telethon import events, Button

from .. import chat_id, jdbot, logger, CONFIG_DIR
from ..bot.utils import V4, AUTH_FILE, press_event, split_list, row, cmd
from ..diy.utils import QL2, ql_token, wskey, read, write

def subcookie(pt_pin, cookie, env):
    if env:
        sh = "/jd/config/config.sh"
        with open(sh, "r", encoding="utf-8") as read:
            configs = read.readlines()
        cknums = []
        for config in configs:
            cknum = re.findall(r'(?<=Cookie)[\d]+(?==")', config)
            if cknum != []:
                m = configs.index(config)
                cknums.append(cknum[0])
                if pt_pin in config:
                    configs[m] = f'Cookie{cknum[0]}="{cookie}"\n'
                    print(f"更新cookie成功！pt_pin：{pt_pin}")
                    break
            elif "第二区域" in config:
                newcknum = int(cknums[-1]) + 1
                configs.insert(m + 1, f'Cookie{newcknum}="{cookie}"\n')
                print(f"新增cookie成功！pt_pin：{pt_pin}")
                break
        with open(sh, "w", encoding="utf-8") as write:
            write.write("".join(configs))
    else:
        config = "/ql/config/auth.json"
        with open(config, "r", encoding="utf-8") as f1:
            token = json.load(f1)['token']
        if exists("/ql/config/env.sh"):
            url = 'http://127.0.0.1:5700/api/envs'
            headers = {'Authorization': f'Bearer {token}'}
            body = {
                'searchValue': pt_pin,
                'Authorization': f'Bearer {token}'
            }
            datas = get(url, params=body, headers=headers).json()['data']
            old = False
            for data in datas:
                if "pt_key" in data['value']:
                    body = {"name": "JD_COOKIE", "value": cookie, "_id": data['_id']}
                    old = True
                    break
            if old:
                put(url, json=body, headers=headers)
                url = 'http://127.0.0.1:5700/api/envs/enable'
                body = [body['_id']]
                put(url, json=body, headers=headers)
                print(f"更新cookie成功！pt_pin：{pt_pin}")
            else:
                body = [{"value": cookie, "name": "JD_COOKIE"}]
                post(url, json=body, headers=headers)
                print(f"新增cookie成功！pt_pin：{pt_pin}")

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^pin=.*;wskey=.*'))
async def myaddwskey(event):
    try:
        text = ""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }        
        msg = await jdbot.send_message(chat_id, "获取到wskey，正在工作中……")
        messages = event.raw_text.split("\n")
        if V4:
            file = f"{CONFIG_DIR}/wskey.list"
        else:
            file = "/ql/db/wskey.list"
        if not os.path.exists(file):
            if V4 or QL2:
                configs = read("str")
                if "wskey" not in configs:
                    sender = event.sender_id
                    async with jdbot.conversation(sender, timeout=120) as conv:
                        tip = "由于这是你第一次使用此功能，关于wskey的存储位置，请做出您的选择："
                        buttons = [
                            Button.inline("存储在config.sh中", data="config.sh"),
                            Button.inline("存储在wskey.list中", data="wskey.list"),
                            Button.inline('取消会话', data='cancel')
                        ]
                        msg = await jdbot.edit_message(msg, tip, buttons=split_list(buttons, row))
                        convdata = await conv.wait_event(press_event(sender))
                        res = bytes.decode(convdata.data)
                        if res == 'cancel':
                            await jdbot.edit_message(msg, '对话已取消')
                            return False
                        elif res == 'wskey.list':
                            os.system(f"touch {file}")
                        msg = await jdbot.edit_message(msg, f'你的选择是：存储在{res}中\n准备继续工作……')
            else:
                token = ql_token(AUTH_FILE)
                url = 'http://127.0.0.1:5700/api/envs'
                headers = {'Authorization': f'Bearer {token}'}
                body = {'searchValue': "JD_WSCK"}
                data = get(url, headers=headers, params=body).json()['data']
                if not data:
                    sender = event.sender_id
                    async with jdbot.conversation(sender, timeout=120) as conv:
                        tip = "由于这是你第一次使用此功能，关于wskey的存储位置，请做出您的选择："
                        buttons = [
                            Button.inline("存储在wskey.list中", data="wskey.list"),
                            Button.inline("存储在环境变量中", data="环境变量"),
                            Button.inline('取消会话', data='cancel')
                        ]
                        msg = await jdbot.edit_message(msg, tip, buttons=split_list(buttons, row))
                        convdata = await conv.wait_event(press_event(sender))
                        res = bytes.decode(convdata.data)
                        if res == 'cancel':
                            await jdbot.edit_message(msg, '对话已取消')
                            return False
                        elif res == 'wskey.list':
                            os.system(f"touch {file}")
                        msg = await jdbot.edit_message(msg, f'你的选择是：存储在{res}中\n准备继续工作……')
        if os.path.exists(file):
            for message in messages:
                ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                pin, key = ws[0], ws[1]
                message = pin + key + ";"
                pt_pin = re.findall(r'pin=(.*);', pin)[0]
                configs = wskey("str")
                if pin + "wskey" in configs:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()                                     
                    try:
                        if res1['code']==200:
                            new_cookie = res1['cookie']
                            configs = re.sub(f'{pin}wskey=.*;', message, configs)
                            if V4:
                                subcookie(pin, new_cookie, True)
                            else:
                                subcookie(pin, new_cookie, False)
                            text += f"更新wskey成功！pin为：{pt_pin}\n更新cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f'你的的wskey貌似过期了！'
                else:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()                          
                    try:
                        if res1['code']==200:
                            new_cookie = res1['cookie']
                            configs = read("str")
                            configs += f"{message}\n"
                            text += f"新增wskey成功！pin为：{pt_pin} \n新增cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f"pin为{pin}的wskey貌似过期了！"                    
                msg = await jdbot.edit_message(msg, text)
                wskey(configs)
        elif V4 or QL2:
            for message in messages:
                ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                pin, key = ws[0], ws[1]
                message = pin + key + ";"
                pt_pin = re.findall(r'pin=(.*);', pin)[0]
                configs = read("str")
                if pin + "wskey" in configs:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()                                     
                    try:
                        if res1['code']==200:
                            new_cookie = res1['cookie']
                            configs = re.sub(f'{pin}wskey=.*;', message, configs)
                            if V4:
                                subcookie(pin, new_cookie, True)
                            else:
                                subcookie(pin, new_cookie, False)
                            text += f"更新wskey成功！pin为：{pt_pin}\n更新cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f'你的的wskey貌似过期了！'
                elif V4 and f"pt_pin={pt_pin}" in configs:
                    configs = read("list")
                    for config in configs:
                        if f"pt_pin={pt_pin}" in config:
                            url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                            res1 = requests.get(url=url1, headers=header).json()   
                            try: 
                                if res1['code']==200:
                                    new_cookie = res1['cookie']
                                    line = configs.index(config)
                                    num = re.findall(r'(?<=[Cc]ookie)[\d]+(?==")', config)[0]
                                    configs.insert(line, f'wskey{str(num)}="{message}"\n')
                                    configs.insert(line, f'Cookie{str(num)}="{new_cookie};"\n')
                                    text += f"更新wskey成功！pin为：{pt_pin}\n更新cookie成功！pt_pin：{pt_pin}\n"
                            except:
                                text += f'你的的wskey貌似过期了！'
                            break
                        elif "第二区域" in config:
                            await jdbot.send_message(chat_id, "请使用标准模板！")
                            return
                elif V4 and f"pt_pin={pt_pin}" not in configs:
                    configs, line, num = read("list"), 0, 0
                    for config in configs:
                        if "pt_pin" in config and "##" not in config:
                            line = configs.index(config) + 1
                            num = int(re.findall(r'(?<=[Cc]ookie)[\d]+(?==")', config)[0]) + 1
                        elif "第二区域" in config:
                            break
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()                                     
                    try:
                        if res1['code']==200:
                            new_cookie = res1['cookie']
                            configs.insert(line, f'Cookie{str(num)}="{new_cookie};"\n')
                            configs.insert(line, f'wskey{str(num)}="{message}"\n')
                            text += f"新增wskey成功！pin为：{pt_pin} \n新增cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f"pin为{pin}的wskey貌似过期了！"
                else:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()                          
                    try:
                        if res1['code']==200:
                            new_cookie = res1['cookie']
                            configs = read("str")
                            configs += f"{message}\n"
                            text += f"新增wskey成功！pin为：{pt_pin} \n新增cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f"pin为{pin}的wskey貌似过期了！"
                msg = await jdbot.edit_message(msg, text)
                write(configs)
        else:
            token = ql_token(AUTH_FILE)
            url = 'http://127.0.0.1:5700/api/envs'
            headers = {'Authorization': f'Bearer {token}'}
            for message in messages:
                ws = re.findall(r'(pin=.*)(wskey=[^;]*);*', message)[0]
                pin, key = ws[0], ws[1]
                message = pin + key + ";"
                pt_pin = re.findall(r'pin=(.*);', pin)[0]
                body = {'searchValue': pin + "wskey="}
                data = get(url, headers=headers, params=body).json()['data']
                if data:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()   
                    try:   
                        if res1['code']==200:
                            body = {"value": message, "name": "JD_WSCK", "_id": data[0]['_id']}
                            put(url, headers=headers, json=body)
                            subcookie(pin, new_cookie, False)
                            text += f"更新wskey成功！pin为：{pt_pin}\n更新cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f"pin为{pin}的wskey貌似过期了！"                    
                else:
                    url1=f'http://api.jdauto.cf/api/w2appck?userid={str(pin.split("=")[1].split(";")[0])}&key={message}'
                    res1 = requests.get(url=url1, headers=header).json()   
                    try:  
                        if res1['code']==200:
                            body = [{"name": "JD_WSCK", "value": message}]
                            code = post(url, json=body, headers=headers).json()['code']
                            if code == 500:
                                post(url, headers=headers, json=body[0])
                            subcookie(pin, new_cookie, False)
                            text += f"新增wskey成功！pin为：{pt_pin} \n新增cookie成功！pt_pin：{pt_pin}\n"
                    except:
                        text += f"pin为{pin}的wskey貌似过期了！"                                
                msg = await jdbot.edit_message(msg, text)

    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"pin为{pin}的wskey貌似过期了！")
        logger.error(f"错误--->{str(e)}")
