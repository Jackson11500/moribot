# import nonebot


from nonebot import get_driver, permission

from .config import Config

from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

global_config = get_driver().config
config = Config(**global_config.dict())

from nonebot.permission import SUPERUSER

#初始函数
def isallow(group,level):#检验许可
    import numpy as np
    if np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()[group]<level:
        return False
    else: 
        return True


##参数
img_path = "file:///D://QQ//Bot//定向回复//"

##az|啊这
chat = on_regex("^az$", priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
    from random import choice
    msg = choice(['啊这','别az了，你只会az吗？',MessageSegment.at(event.user_id)+'你又在az了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
chat = on_regex("^啊这$", priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
    from random import choice
    msg = choice(['az','别啊这了，你只会啊这吗？',MessageSegment.at(event.user_id)+'你又在啊这了，休息一下好不好'])
    await bot.send(event=event,message=msg)
    await chat.finish()


##?
chat = on_regex("^？$|^问号$|^\?$",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
        
    from random import choice
    at = MessageSegment.at(event.user_id)
    msg = choice(['?','？',"问号","需要茉莉酱帮忙吗？","有想问的直接说出来啊，扭扭捏捏地干什么","需要我帮你查核心数据库吗？", 
        at+"在纠结些什么呢？",MessageSegment.image(img_path+"问号//a (1).jpg"),MessageSegment.image(img_path+"问号//a (2).jpg"),
        MessageSegment.image(img_path+"问号//a (3).jpg"),MessageSegment.image(img_path+"问号//a (1).png")])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##草
chat = on_regex("^草$|^艹$",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
        
    from random import choice
    at = MessageSegment.at(event.user_id)
    msg = choice(['草','艹',"茉莉知道！这是一种禾本科植物","你知道吗，草的专业名称是Poaceae","是什么让你这么震惊呢？", 
        "震撼"+at,"我知道我知道，你想说的是这个吧\ngrass = new Floor(\"grass\"){{\n   attributes.set(Attribute.water, 0.1f);\n}};"])
    await bot.send(event=event,message=msg)
    await chat.finish()
    
##贴贴
chat = on_regex("^茉莉贴贴$|^贴贴茉莉$",priority=5,block=True)

@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
        
    from random import choice
    msg = choice(['贴贴！！','贴，都可以贴~',"你太变态了，我不要","好啦，真是拿你没办法呢~贴~","我喜欢你，我们贴贴吧！", \
    "贴什么贴.....只......只能......一下哦！","贴...贴贴（靠近）","蹭蹭…你以为咱会这么说吗！baka死宅快到一边去啦！",\
    "你把脸凑这么近，咱会害羞的啦Σ>―(〃°ω°〃)♡→","小步跑开","达咩~",\
    MessageSegment.image(img_path+"贴贴//被贴贴.jpg"),MessageSegment.image(img_path+"贴贴//贴贴.jpg"),MessageSegment.image(img_path+"贴贴//贴.jpg"),\
    MessageSegment.image(img_path+"贴贴//很奇怪.jpg"),MessageSegment.image(img_path+"贴贴//抱抱.jpg")])
    await bot.send(event=event,message=msg)
    await chat.finish()

moriat = on_message(rule = to_me(),priority=5,block=True)

@moriat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await chat.finish()
    
    #发情模式
    msg=str(event.message)
    if isallow(event.group_id,3):
        import numpy as np
        import random
        chatlist = np.load('D://QQ//Bot//nonebot//moribot//src//plugins//chatting//chatlist.npy',allow_pickle=True).item()
        if msg in chatlist:
            returnmsg=random.choice(chatlist[msg])
            await bot.send(event=event,message=returnmsg)
            await chat.finish()    
    
    #正常模式
    from random import choice
    msg = choice(['不要@我，我...会手足无措的','[非标准命令格式，读取失败]',"[正在数据库寻找合理回复，搜索中..搜索中...Zzzzzz] ",
    "我能感受你想找我聊天啦！ ", "好啦好啦，我都知道了~", "@什么@，仙狐大人也是你能@的吗？", "找我会不会有很重要的事呢？一定要及时报告主人",
    "心烦意乱 惴惴不安 惶恐不安 提心吊胆","要查数据库好好查，@来@去成何体统","@关键词是没有用的！直接问就行了","是...在找我吗？",
    MessageSegment.image(img_path+"@//1.jpg"),MessageSegment.image(img_path+"@//12.jpg"),MessageSegment.image(img_path+"@//服务器无响应.jpg"),
    MessageSegment.image(img_path+"@//咳咳咳喵.jpg"),MessageSegment.image(img_path+"@//女仆.jpg"),MessageSegment.image(img_path+"@//偷瞄.jpg"),
    MessageSegment.image(img_path+"@//自闭模式.jpg")
    ])  
    await bot.send(event=event,message=msg)
    await chat.finish()    
    
##贴贴
'''
不要@我，我...会手足无措的
|[非标准命令格式，读取失败]
|[正在数据库寻找合理回复，搜索中..搜索中...Zzzzzz] 
|我能感受你想找我聊天啦！
|好啦好啦，我都知道了
|@什么@，仙狐大人也是你能@的吗？
|找我会不会有很重要的事呢？一定要及时报告主人
|心烦意乱 惴惴不安 惶恐不安 提心吊胆
|要查数据库好好查，@来@去成何体统
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\服务器无响应.jpg}
|@关键词是没有用的！直接问就行了
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\这点事.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\女仆.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\咳咳咳喵.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\自闭模式.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\偷瞄.jpg}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\1.png}
|{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\@\12.jpg}
async def _poke_me(bot: Bot, event: Event, state: dict):
    return (event.detail_type == 'notify' and event.sub_type == 'poke' and
            str(event.raw_event['target_id']) == bot.self_id)

poke_me = on_notice(_poke_me, priority=10)

@poke_me.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await poke_me.finish("SSS")
        
    from random import choice
    msg = choice(['是在@我吗？'])
    await bot.send(event=event,message=msg)
    await poke_me.finish("AAA")

'''