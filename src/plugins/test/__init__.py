# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

###
moritest = on_command("茉莉代码测试", priority=3, permission=SUPERUSER,block=True)

@moritest.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.user_id !=853330464:
        return 0
    if event.message_type == "private":
        img_path = "file:///D://QQ//Bot//nonebot//moribot//定向回复//+10.jpg"
        
        await bot.send(event=event,message=MessageSegment.image(file = img_path+""))
        await moritest.finish()
    else:
        if event.group_id == "180707407":
            await moritest.finish(str(event.user_id))

    