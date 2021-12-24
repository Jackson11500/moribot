# import nonebot
from nonebot import get_driver
from nonebot.plugin import on_startswith

global_config = get_driver().config

from nonebot import on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment
###
#moritest = on_startswith("测试", priority=3, permission=SUPERUSER,block=True)
async def _poke_me(bot: Bot, event: Event, state: dict):
    return event.notice_type == 'notify' and event.sub_type == 'poke' and str(event.target_id) == bot.self_id

moritest = on_notice(_poke_me, priority=10,block=True)
#moritest = on_message(rule = to_me(),permission=SUPERUSER,priority=10)

@moritest.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    #await bot.send(event,message="茉莉学习中")
    if event.sender_id !=853330464:
        return 0
    #await bot.send(event,message="茉莉学习中")
    #await bot.send(event,message=str(MessageSegment.poke(event.notice_type,853330464)))
    #await bot.send(event,message=MessageSegment.json('[CQ:poke,qq=853330464]'))
    '''
    if event.message_type == "private":
        await moritest.finish()
    elif event.message_type == "group":
        await moritest.finish()
    '''

    