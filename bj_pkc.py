from telethon import events
from .. import user,chat_id
import requests

#私聊狗哥https://t.me/wogouge获取token
user_token=''

'''
#用法
1、先去私聊狗哥号https://t.me/wogouge私发 注册 获取token,填写到上方

2、回复一个带京东链接、淘宝链接、淘宝口令的消息 比价，拉取历史比价数据

3、有任何使用问题反馈给狗哥https://t.me/wogouge
'''

@user.on(events.NewMessage(pattern=r'^bj', outgoing=True))
async def bj_bot(event):
    msg_text = await event.get_reply_message() 
    await event.edit('** [🐶哥](@wogouge) 比价接口** \n正在为你拉取历史比价信息......') 
    messages=str(msg_text).split("message='")[1].split("',",1)[0]
    messages=  messages.split("\n")    
    SuperConvertUrl=''
    for message in messages:
        if "u.jd.com" in message or "item.jd.com" in message or "item.m.jd.com" in message or "kpl.m.jd.com" in message or '₴' in message or '₵' in message or '£' in message or '€' in message or '₤' in message or ' ' in message or '(' in message or ")" in message or "￥" in message or "$" in message or "₳" in message or "¢" in message or "m.tb.cn" in message or "?" in message:
            SuperConvertUrl=message
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    url=f'http://api.jdauto.cf/api/SuperConvert?id={chat_id}&user_token={user_token}&key={SuperConvertUrl}'       
    res = requests.get(url=url, headers=header).json()
    await event.edit(f"{res['tips']}")

    
    



