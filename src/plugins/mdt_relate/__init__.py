# import nonebot


from nonebot import get_driver, permission

from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

global_config = get_driver().config

from nonebot.permission import SUPERUSER
from src.plugins.__toolbox import isallow

##参数
img_path = "file:///D://QQ//Bot//定向回复//"

##卷地蓝
chat = on_regex("卷地蓝",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice(['地蓝人滚出mdt！','你又要开始了卷是ma？','地蓝人来了快跑~',MessageSegment.image(img_path+"卷地蓝.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##
chat = on_regex("戴森球工厂|塑钢带工厂",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice(['戴森球计划要火！',MessageSegment.image(img_path+"戴森球工厂.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()

##
chat = on_regex("(发现|找到)*bug",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice(["It's Not a Bug, It's a Feature",'这是特性！',MessageSegment.image(img_path+"故意的.jpg")])
    await bot.send(event=event,message=msg)
    await chat.finish()

##
chat = on_regex("燃起来了",priority=5,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice([MessageSegment.image(img_path+"草泥马燃起来了.jpg"),MessageSegment.image(img_path+"燃起来了.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##
chat = on_regex("没啥用",priority=5,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice([MessageSegment.image(img_path+"没啥用.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##
chat = on_regex("水边抽水",priority=5,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice([MessageSegment.image(img_path+"这就叫细节.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()

##
chat = on_regex("mdt*(滚|不玩)",priority=5,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await chat.finish()
    from random import choice
    msg = choice([MessageSegment.image(img_path+"mdt滚.png")])
    await bot.send(event=event,message=msg)
    await chat.finish()