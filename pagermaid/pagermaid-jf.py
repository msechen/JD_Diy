#安装脚本前，修改20行bot的用户名xxxxx_bot，使用人形apt -install命令安装脚本
#使用方法，基于人形命令全局回复商品链接-jf，自动返回转链结果
import asyncio
from pagermaid import bot
from pagermaid.listener import listener
from pagermaid.utils import obtain_message, alias_command

@listener(is_plugin=True, outgoing=True, command=alias_command("jf"),
          description="京粉返利（青龙/v4 bot）",
          parameters="<index>")
async def stats(context):
    await context.edit("获取中 . . .")
    reply = await context.get_reply_message()
    try:
        message = await obtain_message(context)
    except ValueError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    #下面这行bot修改成私有bot的用户名
    async with bot.conversation('xxxxx_bot') as conversation:
        await conversation.send_message('/jf ' + message)
        await asyncio.sleep(6)
        chat_response = await conversation.get_response()
        await bot.send_read_acknowledge(conversation.chat_id)
    if reply:
        await context.respond(chat_response, reply_to=reply)
    else:
        await context.respond(chat_response)
    await context.delete()
