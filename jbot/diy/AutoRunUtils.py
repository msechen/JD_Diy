#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import requests
import os
import time
import json
import re

from .. import chat_id, jdbot, CONFIG_DIR
from ..bot.utils import V4, QL, mycron, press_event, AUTH_FILE, cron_manage_QL, add_cron_V4, get_cks, CONFIG_SH_FILE

with open(f"{CONFIG_DIR}/diybotset.json", 'r', encoding='utf-8') as f:
    diybotset = json.load(f)
my_chat_id = int(diybotset['my_chat_id'])


def myids(values, test_id):
    if "," in values:
        ids = values.replace(" ", "").split(",")
        ids = list(map(int, ['%s' % int(_) for _ in ids]))
    else:
        ids = [int(values)]
    ids.append(int(test_id))
    return ids


myzdjr_chatIds = myids(diybotset['myzdjr_chatId'], my_chat_id)

myjoinTeam_chatIds = myids(diybotset['myjoinTeam_chatId'], my_chat_id)

shoptokenIds = myids(diybotset['shoptokenId'], my_chat_id)

listenerIds = myids(diybotset['listenerId'], my_chat_id)

QL8, QL2 = False, False
if os.path.exists('/ql/config/env.sh'):
    QL8 = True
else:
    QL2 = True


# 读取autoconfig.sh
def readauto(arg):
    if arg == "str":
        with open(f"{CONFIG_DIR}/autoconfig.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        return configs
    elif arg == "list":
        with open(f"{CONFIG_DIR}/autoconfig.sh", 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        return configs


# 写入autoconfig.sh
def writeauto(configs):
    if isinstance(configs, str):
        with open(f"{CONFIG_DIR}/autoconfig.sh", 'w', encoding='utf-8') as f1:
            f1.write(configs)
    elif isinstance(configs, list):
        with open(f"{CONFIG_DIR}/autoconfig.sh", 'w', encoding='utf-8') as f1:
            f1.write("".join(configs))
