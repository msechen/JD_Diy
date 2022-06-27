#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
import re
import sys
from asyncio import exceptions

from telethon import events, Button

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import press_event, V4, cmd, TASK_CMD
from ..diy.utils import read, write

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'(zd )'))
async def myaddzd(event):
    try:
        SENDER = event.sender_id
        messages = event.raw_text.split("\n")
        for message in messages:
            if "zd " not in message:
                continue
            
            kname = "jd_zdjr_Code"
            vname = message.replace("zd ", "")
            await jdbot.send_message(chat_id, f"设置变量为：{kname}=\"{vname}\"")
            configs = read("str")
            await asyncio.sleep(0.5)
            
            if f"export {kname}=" in configs:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', f'{kname}="{vname}"', configs)
                end = "替换环境变量成功"
            else:
                note = ''
                configs = read("str")
                configs += f'\nexport {kname}="{vname}"{note}'
                await asyncio.sleep(0.5)
                end = "新增环境变量成功"
            write(configs)
            await asyncio.sleep(0.5) 
            await jdbot.send_message(chat_id, end)
            
            RunCommound="/ql/scripts/ModScript/ccwav_New_jd_zdjr.js"
            await jdbot.send_message(chat_id, '开始执行ccwav_New_jd_zdjr.js，请稍后...')
            await cmd('{} {}'.format(TASK_CMD, RunCommound))
            
    except exceptions.TimeoutError:
        await jdbot.edit_message(chat_id, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")

if ch_name:
    jdbot.add_event_handler(myaddzd, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))