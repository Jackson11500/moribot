# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

accept_group = [180707407,931790051,697981760]
accept_group_test = [180707407,931790051]

###每日重启
user_restart = on_command("每日重启",rule=to_me(), priority=1, permission=SUPERUSER,block=True)

@user_restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.command as command
    msg = command.reboot()
    await bot.send(event=event,message=msg)
    await user_restart.finish("")
    
###签到
user_signin = on_command("签到", priority=1,block=True)

@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.command as command
    if event.group_id not in accept_group:
        return 0
    msg,score = command.user_sign_in(event.user_id)
    if score == 10:
        await bot.send(event=event,message=MessageSegment.image(file = "file:///D://QQ//Bot//nonebot//moribot//定向回复//+10.jpg"))
    await bot.send(event=event,message=MessageSegment.reply(event.message_id)+msg)
    await user_signin.finish()

