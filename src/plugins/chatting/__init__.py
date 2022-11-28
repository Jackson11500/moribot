# import nonebot
from nonebot import get_driver, permission

from .config import Config

from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PRIVATE,PRIVATE_FRIEND

from nonebot.adapters.onebot.v11 import Bot,Event,MessageSegment,PokeNotifyEvent,GroupMessageEvent

global_config = get_driver().config
config = Config(**global_config.dict())

from src.plugins.__toolbox import isallow,checkallow

import os
from configs.path_config import RIMAGE_PATH,PLUGINS_PATH
THIS_PATH = os.path.join(PLUGINS_PATH,'chatting')

##参数
chat_priority = 10
##戳一戳
async def _poke_me(bot: Bot, event: Event):
    return event.notice_type == 'notify' and event.sub_type == 'poke' and str(event.target_id) == bot.self_id

pokeme = on_notice(_poke_me, priority=chat_priority,block=True)

@pokeme.handle()
async def handle_first_receive(bot: Bot, event: PokeNotifyEvent, state: T_State):
    if event.group_id != None:
        await pokeme.finish()
    from random import choice
    msg = choice(['唔...别摸了，毛都要给撸秃了','摸起来舒服吗',"不行那里不可以(´///ω/// `)","变态！！不许乱摸","好吧~_~，就一下下哦……唔~好了……都两下了……(害羞)", "真是好奇怪的要求的说～","温柔一点哦"])
    await bot.send(event=event,message=msg)
    await pokeme.finish()

##az|啊这
chat = on_regex("^az$", priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    from random import choice
    msg = choice(['啊这','别az了，你只会az吗？',MessageSegment.at(event.user_id)+'你又在az了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
chat = on_regex("^啊这$", priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    from random import choice
    msg = choice(['az','别啊这了，你只会啊这吗？',MessageSegment.at(event.user_id)+'你又在啊这了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()

##?
chat = on_regex("^？$|^问号$|^\?$",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    import random
    at = MessageSegment.at(event.user_id)
    ranmsg = ['?','¿','？','(。´・ω・)ん?',"问号","需要茉莉酱帮忙吗？","有想问的直接说出来啊，扭扭捏捏地干什么","需要我帮你查核心数据库吗？", 
        at+"在纠结些什么呢？"]
    title = "问号"
    filelist = [x for x in os.listdir(os.path.join(RIMAGE_PATH,title)) if os.path.isfile(os.path.join(RIMAGE_PATH,title,x))]
    if random.random() < len(ranmsg)/(len(ranmsg)+len(filelist)):
        msg = random.choice(ranmsg)
    else:
        msg = MessageSegment.image(file = "file:///"+os.path.join(RIMAGE_PATH,title,filelist[random.randrange(1,len(filelist),1)]))
    await bot.send(event=event,message=msg)
    await chat.finish()

##草
chat = on_regex("^草$|^艹$",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    from random import choice
    at = MessageSegment.at(event.user_id)
    msg = choice(['草','艹',"茉莉知道！这是一种禾本科植物","你知道吗，草的专业名称是Poaceae","是什么让你这么震惊呢？", 
        "震撼"+at,"我知道我知道，你想说的是这个吧\ngrass = new Floor(\"grass\"){{\n   attributes.set(Attribute.water, 0.1f);\n}};"])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##贴贴
chat = on_regex("^茉莉贴贴$|^贴贴茉莉$",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    import random
    at = MessageSegment.at(event.user_id)
    ranmsg = ['贴贴！！','贴，都可以贴~',"你太变态了，我不要","好啦，真是拿你没办法呢~贴~","我喜欢你，我们贴贴吧！",
    "贴什么贴.....只......只能......一下哦！","贴...贴贴（靠近）","蹭蹭…你以为咱会这么说吗！baka死宅快到一边去啦！",
    "你把脸凑这么近，咱会害羞的啦Σ>―(〃°ω°〃)♡→","小步跑开","达咩~"]
    title = "贴贴"
    filelist = [x for x in os.listdir(os.path.join(RIMAGE_PATH,title)) if os.path.isfile(os.path.join(RIMAGE_PATH,title,x))]
    if random.random() < len(ranmsg)/(len(ranmsg)+len(filelist)):
        msg = random.choice(ranmsg)
    else:
        msg = MessageSegment.image(file = "file:///"+os.path.join(RIMAGE_PATH,title,filelist[random.randrange(1,len(filelist),1)]))
    await bot.send(event=event,message=msg)
    await chat.finish()

##贴贴
chat = on_regex("^吸狐狸$",priority=chat_priority,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
    await bot.send(event=event,message=MessageSegment.image("file:///"+RIMAGE_PATH+"吸狐狸.jpg"))
    await chat.finish()

##贴贴
chat = on_regex("火星了",priority=chat_priority,block=True)
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    await bot.send(event=event,message=MessageSegment.image("file:///"+RIMAGE_PATH+"火星了.jpg"))
    await chat.finish()

##
chat = on_regex("(^寄吧$)|(^几把$)",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    from random import choice
    msg = choice([MessageSegment.image("file:///"+os.path.join(RIMAGE_PATH,"几把","1.jpg")),MessageSegment.image("file:///"+os.path.join(RIMAGE_PATH,"几把","2.jpg")),'不可以说脏话~'])
    await bot.send(event=event,message=msg)
    await chat.finish()

##
chat = on_regex("(^随机涩图$)|(^随机色图$)",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    from random import choice
    msg = choice(['不可以色色~~','茉莉是不可能加这个功能的！','你在想些什么呢baka','唔~死宅真恶心~',
                  '没有！只能把你变成色图',MessageSegment.image("file:///"+os.path.join(RIMAGE_PATH,"不许色色.jpg"))])
    await bot.send(event=event,message=msg)
    await chat.finish()

##
chat = on_regex("笨蛋",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    from random import choice
    await bot.send(event=event,message=MessageSegment.image("file:///"+os.path.join(RIMAGE_PATH,choice(["找笨蛋.jpg","小笨蛋.jpg"]))))
    await chat.finish()

##
chat = on_regex("^救命啊$",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    from random import choice
    await bot.send(event=event,message=MessageSegment.image("file:///"+os.path.join(RIMAGE_PATH,"救命啊.jpg")))
    await chat.finish()

chat = on_regex("114514|1919810|哼哼啊啊啊",priority=chat_priority,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    import random
    at = MessageSegment.at(event.user_id)
    ranmsg = []
    title = "哼哼啊"
    filelist = [x for x in os.listdir(os.path.join(RIMAGE_PATH,title)) if os.path.isfile(os.path.join(RIMAGE_PATH,title,x))]
    if random.random() < len(ranmsg)/(len(ranmsg)+len(filelist)):
        msg = random.choice(ranmsg)
    else:
        msg = MessageSegment.image(file = "file:///"+os.path.join(RIMAGE_PATH,title,filelist[random.randrange(1,len(filelist),1)]))
    await bot.send(event=event,message=msg)
    await chat.finish()

#@茉莉
moriat = on_message(rule = to_me(),priority=chat_priority,block=True)

@moriat.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    if checkallow(event,'chatting')==0:
        await chat.finish()
        
    import json
    data = json.loads(event.json())
    if not data["reply"] == None or not  '[CQ:at,qq=2383008038]' in data["raw_message"]:
        await chat.finish()    
        
    import numpy as np
    import random
    chatlist = np.load(os.path.join(THIS_PATH,'chatlist2.npy'),allow_pickle=True).item()
    msg=str(event.message)
    if msg in chatlist:
        returnmsg=random.choice(chatlist[msg])
        await bot.send(event=event,message=returnmsg)
        await chat.finish()    
            
    #正常模式
    at = MessageSegment.at(event.user_id)
    ranmsg = ['不要@我，我...会手足无措的','[非标准命令格式，读取失败]',"[正在数据库寻找合理回复，搜索中..搜索中...Zzzzzz] ",
    "我能感受你想找我聊天啦！ ", "好啦好啦，我都知道了~", "@什么@，仙狐大人也是你能@的吗？", "找我会不会有很重要的事呢？一定要及时报告主人",
    "心烦意乱 惴惴不安 惶恐不安 提心吊胆","要查数据库好好查，@来@去成何体统","@关键词是没有用的！直接问就行了","是...在找我吗？",]
    title = "@"
    filelist = [x for x in os.listdir(os.path.join(RIMAGE_PATH,title)) if os.path.isfile(os.path.join(RIMAGE_PATH,title,x))]
    if random.random() < len(ranmsg)/(len(ranmsg)+len(filelist)):
        msg = random.choice(ranmsg)
    else:
        msg = MessageSegment.image(file = "file:///"+os.path.join(RIMAGE_PATH,title,filelist[random.randrange(1,len(filelist),1)]))
    
    await bot.send(event=event,message=msg)
    await chat.finish()    