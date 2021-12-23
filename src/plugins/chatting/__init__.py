# import nonebot


from nonebot import get_driver

from .config import Config

from nonebot import on_command
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

global_config = get_driver().config
config = Config(**global_config.dict())

##参数
accept_group = [180707407,931790051,697981760,904318344,740835470]
img_path = "file:///D://QQ//Bot//定向回复//"

##az|啊这
chat = on_command("az", priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    from random import choice
    msg = choice(['啊这','别az了，你只会az吗？',MessageSegment.at(event.user_id)+'你又在az了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
chat = on_command("啊这", priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    from random import choice
    msg = choice(['az','别啊这了，你只会啊这吗？',MessageSegment.at(event.user_id)+'你又在啊这了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()


##?
chat = on_command("?",aliases={"？","问号"},priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    from random import choice
    at = MessageSegment.at(event.user_id)
    msg = choice(['?','？',"问号","需要茉莉酱帮忙吗？","有想问的直接说出来啊，扭扭捏捏地干什么","需要我帮你查核心数据库吗？", 
        at+"在纠结些什么呢？",MessageSegment.image(img_path+"?//(1).jpg"),MessageSegment.image(img_path+"?//(2).jpg"),\
        MessageSegment.image(img_path+"?//(3).jpg"),MessageSegment.image(img_path+"?//(1).png")])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##草
chat = on_command("草",aliases={"艹"},priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    from random import choice
    at = MessageSegment.at(event.user_id)
    msg = choice(['草','艹',"茉莉知道！这是一种禾本科植物","你知道吗，草的专业名称是Poaceae","是什么让你这么震惊呢？", 
        "震撼"+at,"我知道我知道，你想说的是这个吧\ngrass = new Floor(\"grass\"){{\n   attributes.set(Attribute.water, 0.1f);\n}};"])
    await bot.send(event=event,message=msg)
    await chat.finish()
    

##贴贴
chat = on_command("茉莉贴贴",aliases={"贴贴茉莉"},priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    from random import choice
    msg = choice(['贴贴！！','贴，都可以贴~',"你太变态了，我不要","好啦，真是拿你没办法呢~贴~","我喜欢你，我们贴贴吧！", \
    "贴什么贴.....只......只能......一下哦！","贴...贴贴（靠近）","蹭蹭…你以为咱会这么说吗！baka死宅快到一边去啦！",\
    "你把脸凑这么近，咱会害羞的啦Σ>―(〃°ω°〃)♡→","小步跑开","达咩~",\
    MessageSegment.image(img_path+"贴贴//被贴贴.jpg"),MessageSegment.image(img_path+"贴贴//贴贴.jpg"),MessageSegment.image(img_path+"贴贴//贴.jpg"),\
    MessageSegment.image(img_path+"贴贴//很奇怪.jpg"),MessageSegment.image(img_path+"贴贴//抱抱.jpg")])
    await bot.send(event=event,message=msg)
    await chat.finish()




'''
{群消息,{随机值,
贴贴！！
|贴，都可以贴~
|你太变态了，我不要
|好啦，真是拿你没办法呢~贴~
|我喜欢你，我们贴贴吧！
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\很奇怪.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\抱抱.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\贴贴.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\贴.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\被贴贴.jpg}
}
}

{随机值,
艹
|草
|茉莉知道！这是一种禾本科植物
|你知道吗，草的专业名称是Poaceae
|是什么让你这么震惊呢
|震撼 {@,{QQ}}
|我知道我知道，你想说的是这个吧{换行}{文本删空行,{读文本,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\mdt-数据\type\grass}}
}
{群消息,{随机值,
在纠结些什么呢？
|需要茉莉酱帮忙吗？
|有想问的直接说出来啊，扭扭捏捏地干什么
|？
|需要我帮你查核心数据库吗？
|?
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\？.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\2.png}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\？2.jpg}
}
}

'''