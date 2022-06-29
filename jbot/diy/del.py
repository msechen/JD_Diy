#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio, datetime, os, re, sys, time, json, requests
from unittest import result
from telethon import events
from urllib import parse
from .user import client

@client.on(events.NewMessage(pattern=r'^d[ 0-9]*$', incoming=True, outgoing=True))
async def del_msg(event):
    try:
        num = event.raw_text.split(' ')
        if isinstance(num, list) and len(num) == 2:
            count = int(num[-1])
        else:
            count = 10
        await event.delete()
        count_buffer = 0
        async for message in client.iter_messages(event.chat_id, from_user="me"):
            if count_buffer == count:
                break
            await message.delete()
            count_buffer += 1
        notification = await client.send_message(event.chat_id, f'已删除{count_buffer}/{count}')
        time.sleep(.5)
        await notification.delete()
    except Exception as e:
        await client.send_message(event.chat_id, str(e))