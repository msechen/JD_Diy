#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By ccwav 20220517

import os
import re
import traceback
import asyncio
from telethon import events
import time
import datetime
from .login import user
from .utils import execute
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import TASK_CMD, cmd
from ..diy.utils import myzdjr_chatIds, read, write
from ..diy.AutoRunUtils import readauto, writeauto

from cacheout import FIFOCache
cache = FIFOCache(maxsize=5)
cache2 = FIFOCache(maxsize=100)
bot_id = int(TOKEN.split(":")[0])
client = user

@client.on(events.NewMessage(from_users=chat_id, pattern=r"^user(\?|？)$"))
async def user(event):
    try:
        await event.edit(r'查毛线查，ccwav写的监控你担心个屁！！')
    except Exception as e:
        title = ""
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(
            chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")

@client.on(events.NewMessage(from_users=chat_id, pattern=r'^reuser'))
async def reuser(event):
    try:
        AutoConfigs = readauto("str")
        TempAutoConfigs = AutoConfigs.split("\n")
        change=""
        for AutoConfigline in TempAutoConfigs: 
            if "export " not in AutoConfigline:                
                continue           
            kv = AutoConfigline.replace("export ", "")           
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
            if value == "YES":
                kv=f'{key}="NO"'
                AutoConfigs = re.sub(f'{key}=("|\').*("|\')', kv, AutoConfigs)
                change += f"【重置】 `{key}` 任务状态成功: `{kv}`\n\n"  
                writeauto(AutoConfigs)
        if change=="":
            await event.edit("所有监控任务都是等待状态，不需要重置!")
        else:
            await event.edit(change)
        
    except Exception as e:
        title = ""
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(
            chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
@client.on(events.NewMessage(chats=myzdjr_chatIds, pattern=r'export\s(jd_zdjr_|invite_code|QITOQITO|M_|WDZactivityId|comm_activityIDList|wish_appNameArrList|video_activityUrl|jd_mhurlList|fav_and_add_cart_activityId|jd_nzmhurl|wish_appIdArrList|computer_activityIdList|shareActivityId).*=(".*"|\'.*\')'))
async def activityID(event):
    try:        
        name = ""
        text = event.message.text        
        strAutoTask=""
        lnError=0
        lniscj=0
        
        if "cjhy" in text:
            lniscj=1
            
        if "M_WX_ADD_CART_URL" in text:           
            name = "M加购有礼"
            strAutoTask="AutoTaskAddCard" 
        elif "M_WX_POINT_DRAW_URL" in text: 
            name = "M积分兑换"
            strAutoTask="AutoTaskPOINTDRAW"
        elif "M_WX_SHOP_GIFT_URL" in text:
            name = "M关注有礼-无线"
            strAutoTask="AutoTaskFOLLOWSHOP" 
        elif "M_FOLLOW_SHOP_ARGV" in text:
            name = "M关注有礼"
            # strAutoTask="AutoTaskFOLLOWSHOP"
        elif "M_FANS_RED_PACKET_URL" in text:
            name = "M粉丝红包"
            strAutoTask="AutoTaskFansRed"  
        elif "HDID" in text:   
            # 这个注释掉了
            name = "rush福袋" 
            strAutoTask="AutoTaskUNPACKDRAW"
        elif "M_WX_UNPACK_DRAW_URL" in text:
            name = "M分享福袋"
            strAutoTask="AutoTaskUNPACKDRAW"    
        elif "jd_zdjr_" in text:
            name = "组队瓜分"
            if lniscj==1:
                strAutoTask="AutoTaskZdcj"   
            else:
                strAutoTask="AutoTaskZdlj"            
        elif "ACTIVITY_ID" in text:
            # 这个注释掉了
            name = "分享有礼"
            strAutoTask="AutoTaskShare1"
        elif "M_WX_SHARE_URL" in text:
            name = "M分享有礼"
            strAutoTask="AutoTaskShare1"            
        elif "shareActivityId" in text:
            name = "分享礼包"
            strAutoTask="AutoTaskShare2" 
        elif "wxShareActivity_Id" in text:
            # 这个注释掉了
            name = "rush分享有礼"            
        elif "M_WX_COLLECT_CARD_URL" in text:
            # 这个不跑了,没水还黑IP
            name = "集卡抽奖"
            strAutoTask="AutoTaskCOLLECTCard"               
        
        elif "M_WX_SECOND_DRAW_URL" in text:
            name = "M读秒手速"
            strAutoTask="AutoTaskReadSec"        
        elif "M_OPEN_CARD_ARGV" in text:
            name = "M入会有礼" 
            strAutoTask="AutoTaskOPENCARD"
        elif "M_WX_FOLLOW_DRAW_URL" in text:
            name = "M关注抽奖"
            strAutoTask="AutoTaskLUCK"
        elif "M_WX_CENTER_DRAW_URL" in text:
            name = "M老虎机抽奖"
            strAutoTask="AutoTaskLUCK"
        elif "M_WX_LUCK_DRAW_URL" in text:
            name = "M幸运抽奖"
            strAutoTask="AutoTaskLUCK"
        elif "M_WX_SHOP_SIGN_URL" in text:
            name = "7天签到有礼"
            strAutoTask="AutoTask7Days"
        elif "M_WX_BUILD_DRAW_URL" in text:
            name = "M盖楼领奖"
            strAutoTask="AutoTaskBUILD"            
        elif "M_WX_FANS_DRAW_URL" in text:
            name = "M粉丝互动"
            strAutoTask="AutoTaskDouDouFans"
        elif "WXGAME_ACT_ID" in text:
            #变量暂时注释,用M打豆豆
            name = "打豆豆"
            strAutoTask="AutoTaskDouDouFans"
        elif "M_WX_DADOUDOU_URL" in text:
            name = "M打豆豆"
            strAutoTask="AutoTaskDouDouFans"
        elif "computer_activityIdList" in text:
            name = "电脑配件"            
        elif "comm_activityIDList" in text:
            name = "通用ID任务"
            strAutoTask="AutoTaskactivityIDList"
        elif "wish_appIdArrList" in text:
            strAutoTask="AutoTaskWish"
            name = "众筹许愿池"
        elif "wish_appNameArrList" in text:
            strAutoTask="AutoTaskWish"
            name = "众筹许愿池"    
        elif "jd_mhurlList" in text:
            name = "盲盒任务抽京豆"
        elif "jd_nzmhurl" in text:
            name = "女装盲盒抽京豆"
        elif "fav_and_add_cart_activityId" in text:
            strAutoTask="AutoTaskLHShare"
            name = "联合关注+加购+分享领豆"
        elif "M_TOKEN_SHOP_SIGN" in text:
            name = "店铺签到" 
        elif "M_WX_GAME_URL" in text:
            name = "M无线游戏"
            strAutoTask="AutoTaskWxGame"
        elif "M_WX_DAILY_GIFT_URL" in text:
            name = "M每日领奖"
            #不排队了,不然渣都没了
            #strAutoTask="AutoTaskDAILYGIFT"
        elif "video_activityUrl" in text:
            name = "视频分享领京豆"
        elif "M_GYG_SHOP_ARGV" in text:
            name = "M店铺刮奖"
            strAutoTask="AutoTaskGYG"
        elif "M_FAV_SHOP_ARGV" in text:
            name = "M收藏有礼"
            strAutoTask="AutoTaskARGV"
        elif "WDZactivityId" in text:
            name = "微订制"
            strAutoTask="AutoTaskWDZ"
        # elif "M_COMM_RED_RAIN_ARGV" in text:
            # name = "M通用红包雨"
        elif "M_OPEN_CARD_FORCE_ARGV" in text:
            name = "M强制入会"
            strAutoTask="AutoTaskOPENCARD"
        elif "M_WX_CARTKOI_URL" in text:
            name = "M购物车锦鲤"
            strAutoTask="AutoTaskCARTKOI"
        elif "invite_code" in text:
            name = "邀请赢大礼"
            strAutoTask="AutoTaskYaoQing"
        elif "QITOQITO" in text:
            name = "可达鸭库Token"            
        else:            
            await jdbot.send_message(chat_id, f'监测到环境变量，但是没有任务'+text)
            return
            
        #停止监控代码    
        # if name!="店铺签到" and name!="女装盲盒抽京豆" and name!="盲盒任务抽京豆" and name!="众筹许愿池" and name!="通用ID任务" :
            # return
            
        if lniscj==1:
            await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量(CJ域名)！')
        else:
            await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量(普通域名)！')
        
        if name=="集卡抽奖":
            await jdbot.send_message(chat_id, f"`{name}` 不跑，垃圾活动退出线程！")
            return
            
        if name != "组队瓜分" and name != "7天签到有礼" and name != "M购物车锦鲤" and name!="M幸运抽奖" and name != "M老虎机抽奖" :
            if cache.get(text) is not None:
                await jdbot.send_message(chat_id, f"`{name}` 已经触发过了，退出线程！")
                return
            else:            
                cache.set(text,text)
        
        if name=="M幸运抽奖" or name == "M老虎机抽奖":
            strstarttime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")+" "+'00:00:00' 
            starttime = time.strptime(strstarttime, "%Y-%m-%d %H:%M:%S")
            intstarttime = int(time.mktime(starttime))-int(round(time.time()))
            if (intstarttime)<240:
                #置空变量
                cache.clear();
                cache2.clear();
                configs = read("str")
                key="M_WX_LUCK_DRAW_URL"
                kv=f'{key}=""'
                if kv not in configs:
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                    key="M_WX_CENTER_DRAW_URL"
                    kv=f'{key}=""'
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)                
                    key="M_WX_SHOP_SIGN_URL"
                    kv=f'{key}=""'
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)                
                    key="M_WX_DADOUDOU_URL"
                    kv=f'{key}=""'
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                    key="M_WX_DAILY_GIFT_URL"
                    kv=f'{key}=""'
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                    key="M_WX_CARTKOI_URL"
                    kv=f'{key}=""'
                    configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                    write(configs)
                    await jdbot.send_message(chat_id, f"先置空一堆变量.......")
            if cache2.get(text) is not None:
                await jdbot.send_message(chat_id, f"`{name}` 已经触发过了，退出线程！")
                return
            else:            
                cache2.set(text,text)

        messages = event.message.text.split("\n")
        change = ""
        boolSkip=0
        for message in messages:            
            if "export " not in message:                
                continue           
            kv = message.replace("export ", "")
            #防悲剧:
            if kv!='""':
                kv=kv.replace('""', '"')
                kv=kv.replace('**', '')
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
            
            if (key=="M_WX_DADOUDOU_URL" or key=="WXGAME_ACT_ID") and len(value)<5:
                value=""
            
            if value=="null":
                lnError=1
            if value=="":
                lnError=2
            
            #组队替换成可达鸭    
            if key=="jd_zdjr_activityId":
                if lniscj==1:
                    key="jd_cjzd_custom"
                else:                
                    key="jd_lzd_custom"                    
                kv=f'{key}="{value}"'
                
            #加购替换成可达鸭 
            # if key=="M_WX_ADD_CART_URL":
                # key=="jd_addCard_custom"
                # kv=f'{key}="{value}"'
            
            #微订制替换成可达鸭
            # if key=="WDZactivityId":
                # key=="jd_wdz_custom"
                # kv=f'{key}="{value}"'
                
            if key=="jd_zdjr_activityUrl":
                continue    
            if key=="jd_zdjr_type":
                if "积分" in message:
                    boolSkip=1 
                continue
            intstart=value.find("http")
            if(intstart>0):               
                value=value[intstart:-1]
                kv=f'{key}="{value}"'
            configs = read("str")
            if kv in configs:
                continue
            if key in configs:                
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"                
            else:
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"  
        # if boolSkip==1:
            # await jdbot.send_message(chat_id, f"`{name}` 积分车不跑，退出线程！")
            # return
        if lnError==1:
            await jdbot.send_message(chat_id, "变量的值有问题，逗你玩???\n"+text)
            return
        
        if change=="" and name!="M打豆豆" and name!="女装盲盒抽京豆" and name!="盲盒任务抽京豆" and name!="众筹许愿池" and name!="M每日领奖" and name!="通用ID任务" and name!="7天签到有礼" and name != "组队瓜分" and name != "M购物车锦鲤":            
            await jdbot.send_message(chat_id, f"`{name}` 环境变量没有改变，退出线程！")
            return
            
        if lnError!=2 and strAutoTask!="":
            AutoConfigs = readauto("str")
            tempcheck=f'{strAutoTask}="YES"'
            lncount=0
            while tempcheck in AutoConfigs:    
                if lncount==0:
                    msg=await jdbot.send_message(chat_id, f'`{name}`: 任务占用中,等待30秒....')  
                else:
                    msg=await jdbot.send_message(chat_id, f'`{name}`: 任务占用中,继续等待30秒....')
                lncount=lncount+1
                await asyncio.sleep(30)
                await jdbot.delete_messages(chat_id,msg)
                AutoConfigs = readauto("str")
                
            if strAutoTask in AutoConfigs:
                AutoConfigs = re.sub(f'{strAutoTask}=("|\').*("|\')', tempcheck, AutoConfigs)
            else:
                AutoConfigs = readauto("str")
                AutoConfigs += f'export {strAutoTask}="YES"\n'                      
            writeauto(AutoConfigs)        
            await jdbot.send_message(chat_id, f"标记任务执行变量成功\n`{tempcheck}`\n")
            if name=="M幸运抽奖" or name == "M老虎机抽奖":
                strstarttime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")+" "+'00:00:00' 
                starttime = time.strptime(strstarttime, "%Y-%m-%d %H:%M:%S")
                intstarttime = int(time.mktime(starttime))-int(round(time.time()))
                if (intstarttime)<240:
                    await jdbot.send_message(chat_id,"现在是23:26分之后时段,等待:"+str(intstarttime)+"秒后再触发任务")
                    await asyncio.sleep(intstarttime)
                    
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:            
            if "export " not in message:                
                continue 
            kv = message.replace("export ", "")
            #防悲剧
            if kv!='""':
                kv=kv.replace('""', '"')
                kv=kv.replace('**', '')
            key = kv.split("=")[0]
            if key=="jd_zdjr_activityUrl":
                continue
            if key=="jd_zdjr_type":
                continue
                
            value = re.findall(r'"([^"]*)"', kv)[0]            
            
            if lnError==2:
                value=""
                
            #组队替换成可达鸭    
            if key=="jd_zdjr_activityId":
                if lniscj==1:
                    key="jd_cjzd_custom"
                else:                
                    key="jd_lzd_custom"                    
                kv=f'{key}="{value}"'
                
            #加购替换成可达鸭
            # if key=="M_WX_ADD_CART_URL":
                # key=="jd_addCard_custom"
                # kv=f'{key}="{value}"'
                
            #微订制替换成可达鸭
            # if key=="WDZactivityId":
                # key=="jd_wdz_custom"
                # kv=f'{key}="{value}"'
                
            configs = read("str")            
            if kv in configs:
                continue
                
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"  
                write(configs)
            else:
                configs = read("str")
                configs += f'export {key}="{value}"\n'
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"  
                write(configs)
        if lnError==2:
            await jdbot.send_message(chat_id, f"【置空】 `{name}` 环境变量成功\n`{kv}`\n\n"  ) 
            return
        if change=="" and name!="M打豆豆" and name!="女装盲盒抽京豆" and name!="盲盒任务抽京豆" and name!="众筹许愿池" and name!="M每日领奖" and name!="通用ID任务" and name!="7天签到有礼" and name != "组队瓜分" and name != "M购物车锦鲤":    
            await jdbot.send_message(chat_id, f"`{name}` 环境变量没有改变，取消操作[2]！")
            if strAutoTask!="":
                AutoConfigs = readauto("str")
                tempcheck=f'{strAutoTask}="NO"'
                if strAutoTask in AutoConfigs:
                    AutoConfigs = re.sub(f'{strAutoTask}=("|\').*("|\')', tempcheck, AutoConfigs)
                else:
                    AutoConfigs = readauto("str")
                    AutoConfigs += f'export {strAutoTask}="NO"\n'           
                writeauto(AutoConfigs)
                await jdbot.send_message(chat_id, f"[2]标记任务完成变量成功\n`{tempcheck}`\n")
            return
        try:
            if change!="":
                msg = await jdbot.send_message(chat_id, change)
            if name == "店铺签到":
                #这个任务靠脚本定时跑，不需要触发
                return
            if name=="组队瓜分":
                if lniscj==1:
                    RunCommound="jd_cjzd.js"
                    await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                    await cmd('{} {}'.format(TASK_CMD, RunCommound))
                else:
                    RunCommound="jd_lzd.js"
                    await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                    await cmd('{} {}'.format(TASK_CMD, RunCommound))
                
                # await asyncio.sleep(30)
                
                # configs = read("str")
                # kv=f'TT_wait_common="7000"'
                # key="TT_wait_common"
                # configs = read("str")
                # configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                # change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"                   
                # write(configs)
                
                # RunCommound="/ql/scripts/AutoRun/jd_opencard_teamBean_common_enc_Mod.js desi JD_COOKIE 4 30-70"
                # await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                # await cmd('{} {}'.format(TASK_CMD, RunCommound))
                
                
            elif name == "分享有礼":
                RunCommound="/ql/scripts/AutoRun/ccwav_jd_share.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))       
                
                # await asyncio.sleep(10)
                # RunCommound="/ql/scripts/AutoRun/ccwav_jd_share2.js desi JD_COOKIE 2-70"
                # await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本2，请稍候")
                # await cmd('{} {}'.format(TASK_CMD, RunCommound))
                
                # RunCommound="/ql/scripts/AutoRun/ccwav_jd_share.js desi JD_COOKIE 3-70"
                # await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本2，请稍候")
                # await cmd('{} {}'.format(TASK_CMD, RunCommound))
                
                # RunCommound="/ql/scripts/AutoRun/ccwav_jd_share.js desi JD_COOKIE 4-70"
                # await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本2，请稍候")
                # await cmd('{} {}'.format(TASK_CMD, RunCommound))
                
            elif name == "M分享有礼":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_share.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))       
                
            elif name == "M加购有礼":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_addCart.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "分享礼包":
                RunCommound="/ql/scripts/AutoRun/jd_share.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M收藏有礼":
                RunCommound="/ql/scripts/AutoRun/m_jd_fav_shop_gift.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))            
            elif name == "M入会有礼":
                RunCommound="/ql/scripts/AutoRun/m_jd_open_card.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M强制入会":
                RunCommound="/ql/scripts/AutoRun/m_jd_open_card_force.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))                
            elif name == "集卡抽奖":
                RunCommound="/ql/scripts/AutoRun/jd_card_collecting_common_enc_Mod.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M分享福袋":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_unPackDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M读秒手速":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_secondDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M粉丝互动":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_fansDraw.js desi JD_COOKIE 1-7"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "7天签到有礼":
                # if lniscj==1:
                    # RunCommound="/ql/scripts/AutoRun/m_jd_wx_shopSign.js desi JD_COOKIE 1-5"
                # else:
                    # RunCommound="/ql/scripts/AutoRun/m_jd_wx_shopSign.js"
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_shopSign.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "微订制":
                RunCommound="/ql/scripts/AutoRun/gua_jointeam33.js desi JD_COOKIE 1-100"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
                
            elif name == "M关注抽奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_followDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))                
            elif name == "M老虎机抽奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_centerDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M关注有礼-无线":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_shopGift.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M关注有礼":                
                RunCommound="/ql/scripts/AutoRun/m_jd_follow_shop.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
            elif name == "M粉丝红包":
                RunCommound="/ql/scripts/AutoRun/m_jd_fans_redPackt.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M幸运抽奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_luckDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M无线游戏":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_game.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))   
            elif name == "M店铺刮奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_shop_gyg.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "rush福袋":
                RunCommound="/ql/scripts/AutoRun/rush_wxUnPackingActivity.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "rush分享有礼":
                RunCommound="/ql/scripts/AutoRun/rush_share.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "电脑配件":
                #这个任务靠脚本定时跑，不需要触发
                return
                # RunCommound="/ql/scripts/AutoRun/jd_computer.js"
                # await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                # await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
            elif name == "可达鸭库Token": 
                return 
            elif name == "通用ID任务":
                RunCommound="/ql/scripts/AutoRun/jd_joyjd_open.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "众筹许愿池":
                RunCommound="/ql/scripts/AutoRun/jd_wish.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "盲盒任务抽京豆":
                RunCommound="/ql/scripts/AutoRun/jd_mhtask.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "女装盲盒抽京豆":
                RunCommound="/ql/scripts/AutoRun/jd_nzmh.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
            elif name == "联合关注+加购+分享领豆":
                RunCommound="/ql/scripts/AutoRun/fav_and_addcart.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "打豆豆":
                RunCommound="/ql/scripts/AutoRun/jd_dadoudou.js desi JD_COOKIE 1-30"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M打豆豆":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_dadoudou.js desi JD_COOKIE 1-30"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M每日领奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_dailyGift.js desi JD_COOKIE 1"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
            elif name == "视频分享领京豆":
                RunCommound="/ql/scripts/AutoRun/jd_videoactivity.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M盖楼领奖":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_buildDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))
            elif name == "M积分兑换":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_pointDraw.js"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound)) 
            elif name == "M购物车锦鲤":
                RunCommound="/ql/scripts/AutoRun/m_jd_wx_cartKoi.js desi JD_COOKIE 1-4"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))    
            elif name == "邀请赢大礼":
                RunCommound="/ql/scripts/AutoRun/jd_yqhyydl.py"
                await jdbot.send_message(chat_id, f"开始执行 `{name}` 脚本，请稍候")
                await cmd('{} {}'.format(TASK_CMD, RunCommound))    
                
            if strAutoTask!="":
                AutoConfigs = readauto("str")
                tempcheck=f'{strAutoTask}="NO"'
                if strAutoTask in AutoConfigs:
                    AutoConfigs = re.sub(f'{strAutoTask}=("|\').*("|\')', tempcheck, AutoConfigs)
                else:
                    AutoConfigs = readauto("str")
                    AutoConfigs += f'export {strAutoTask}="NO"\n'           
                writeauto(AutoConfigs)
                await jdbot.send_message(chat_id, f"标记任务完成变量成功\n`{tempcheck}`\n")
            
        except ImportError:
            await jdbot.send_message(chat_id, f"错误了")
            pass
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")       

