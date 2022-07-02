from telethon import events
from .user import client

from .. import jdbot
from .utils import read, write
import re
import requests
@client.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    M_API_TOKEN = "951306588:373af8dc89e801376a35e603cc558a9f"            
    headers = {"token": M_API_TOKEN}
    strText=""
    if event.is_reply is True:
        reply = await event.get_reply_message()
        strText=reply.text
    else:    
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]
    
    if strText==None:
        await client.send_message(event.chat_id,'请指定要解析的口令,格式: jx 口令 或对口令直接回复jx ')
        return    
        
    data = requests.post("http://ailoveu.eu.org:19840/jCommand",
                             headers=headers,
                             json={"code": strText}).json()
    code = data.get("code")
    if code == 200:
        data = data["data"]
        title = data["title"]
        jump_url = data["jumpUrl"]
        await client.send_message(event.chat_id,title+"\n"+jump_url)
    else:
        await client.send_message(event.chat_id,"解析出错:"+data.get("data"))
    
    