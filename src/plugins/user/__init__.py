# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_regex
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import isallow

accept_group = [180707407,931790051,697981760]
accept_group_test = [180707407,931790051]

###每日重启
user_restart = on_regex("^每日重启$", priority=1, permission=SUPERUSER,block=True)

@user_restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.command as command
    msg = command.reboot()
    await bot.send(event=event,message=msg)
    await user_restart.finish("")
    
###签到
user_signin = on_regex("^签到$", priority=2,block=True)

@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.command as command
    if not isallow(event.group_id,1):
        await user_signin.finish()
    msg,score = command.user_sign_in(event.user_id)
    if score == 10:
        msg = MessageSegment.reply(event.message_id)+msg+MessageSegment.image(file = "file:///D://QQ//Bot//定向回复//+10.jpg")
    else:
        msg = MessageSegment.reply(event.message_id)+msg
    await bot.send(event=event,message=msg)
    await user_signin.finish()

###签到
user_signin = on_regex("^注册$", priority=2,block=True)

@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.command as command
    if not isallow(event.group_id,1):
        await user_signin.finish()
    par = command.signup(event.user_id)
    if par == 0:
        msg = MessageSegment.reply(event.message_id)+"茉莉这里已经有你的档案啦，不需要再注册一遍的！"
    else:
        msg = MessageSegment.reply(event.message_id)+f"注册成功！你是第{par}位成为茉莉朋友的人！"
    await bot.send(event=event,message=msg)
    await user_signin.finish()