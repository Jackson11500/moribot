# import nonebot
from nonebot import get_driver
from nonebot.plugin import on_startswith

global_config = get_driver().config

from nonebot import on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment,PrivateMessageEvent
###
#moritest = on_startswith("测试", priority=3, permission=SUPERUSER,block=True)
async def _poke_me(bot: Bot, event: Event, state: dict):
    return event.notice_type == 'notify' and event.sub_type == 'poke' and str(event.target_id) == bot.self_id

#moritest = on_notice(_poke_me, priority=10,block=True)

import json
from random import choice

img_path = "file:///D://QQ//Bot//定向回复//"

def At(data: str):
    """
    检测at了谁
    :param data: event.json
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(int(msg["data"]["qq"]))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return ['null']

moritest = on_command("测试",permission=SUPERUSER,priority=1,block=True)

@moritest.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message="测试开始")
    import sys
    #sys.path.append("D://QQ//Bot//General分支(1.0.1)(1)//General分支(1.0.1)(1)//兔子-db包//用户数据") 
    from src.plugins.user.utils import modify_res
    text = modify_res(11451491919,0,10,10,-500,1)
    await bot.send(event=event,message=str(text))
    await moritest.finish('测试完成')
    '''
    import src.plugins.user.command as command
    msg,score = command.user_sign_in(event.user_id)
    if score == 10:
        msg = MessageSegment.reply(event.message_id)+msg+MessageSegment.image(file = "file:///D://QQ//Bot//定向回复//+10.jpg")
    else:
        msg = MessageSegment.reply(event.message_id)+msg
    await bot.send(event=event,message='茉莉正在重做整理用户系统！将于明年上线正式版，敬请期待\n'+msg)
    await moritest.finish()
    '''

moritest = on_command("",rule = to_me(),priority=1,block=True)

@moritest.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await moritest.finish('')
    '''
    import src.plugins.user.command as command
    msg,score = command.user_sign_in(event.user_id)
    if score == 10:
        msg = MessageSegment.reply(event.message_id)+msg+MessageSegment.image(file = "file:///D://QQ//Bot//定向回复//+10.jpg")
    else:
        msg = MessageSegment.reply(event.message_id)+msg
    await bot.send(event=event,message='茉莉正在重做整理用户系统！将于明年上线正式版，敬请期待\n'+msg)
    await moritest.finish()
    '''

    