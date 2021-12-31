# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_regex
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import isallow

###每日重启
user_restart = on_command("数据备份",rule=endswith("数据备份"), priority=1, permission=SUPERUSER,block=True)

@user_restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.user_data as us
    msg = us.backup()
    await bot.send(event=event,message=msg)
    await user_restart.finish("")
    
###签到
user_signin = on_command("签到",rule=endswith("签到"), priority=3,block=True)
@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    #await bot.send(event=event,message='新用户系统删档测试中...将于2022年正式上线！')
    await bot.send(event=event,message='新用户系统将于2022年1月1日正式上线，敬请期待！')
    await user_signin.finish()
    if not isallow(event,1):
        await user_signin.finish()
    import src.plugins.user.user_data as us
    text = await us.user_sign_in(bot=bot, event=event, state=state)
    import os 
    if (os.path.exists(text)):
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+MessageSegment.image(file = "file:///"+text))
    else:
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+text)
    await user_signin.finish()

###签到
user_register = on_command("注册",rule=endswith("注册"), priority=3,block=True)

@user_register.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message='新用户系统将于2022年1月1日正式上线，敬请期待！')
    await user_signin.finish()
    if not isallow(event,1):
        await user_register.finish()
    import src.plugins.user.user_data as us
    par = us.register(event.user_id)
    if par==0:
        msg = MessageSegment.reply(event.message_id)+"茉莉这里已经有你的档案啦，不需要再注册一遍的！"
    else:
        msg = MessageSegment.reply(event.message_id)+f"注册成功！你是第{par}位成为茉莉朋友的人！"
    await bot.send(event=event,message=msg)
    await user_register.finish()