from telethon import events
import requests,json,os
from ..bot.utils import get_cks
from .. import chat_id, jdbot, logger, API_ID, API_HASH, PROXY_START, proxy, JD_DIR, TOKEN
from urllib import parse
import asyncio
from .user import client

#私聊狗哥获取token
user_token=''

@client.on(events.NewMessage(pattern=r'^bj', outgoing=True))
async def bj_bot(event):
    msg_text = await event.get_reply_message() 
    messages=str(msg_text).split("message='")[1].split("',",1)[0]
    messages=  messages.split("\n")    
    try:
        SuperConvertUrl=''
        for message in messages:
            if "u.jd.com" in message or "item.jd.com" in message or "item.m.jd.com" in message or "kpl.m.jd.com" in message or '₴' in message or '₵' in message or '£' in message or '€' in message or '₤' in message or '�' in message or '(' in message or ")" in message or "￥" in message or "$" in message or "₳" in message or "¢" in message or "m.tb.cn" in message or "?" in message:
                SuperConvertUrl=message
                await event.edit(SuperConvertUrl)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        url=f'http://api.jdauto.cf/api/SuperConvert?id={chat_id}&user_token={user_token}&key={SuperConvertUrl}'       
        res = requests.get(url=url, headers=header).json()
        await event.edit(f"{res['tips']}")
            
    except Exception as e:
        print(e)

    
    



