#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio, datetime, os, re, sys, time, json, requests
from unittest import result
from telethon import events
from urllib import parse
from .user import client

@client.on(events.NewMessage(pattern=r'^re[ 0-9]*$', outgoing=True))
async def mycp(event):
    num = event.raw_text.split(' ')
    if isinstance(num, list) and len(num) == 2:
        num = int(num[-1])
    else:
        num = 1
    reply = await event.get_reply_message()
    await event.delete()
    for _ in range(0, num):
        await reply.forward_to(int(event.chat_id))