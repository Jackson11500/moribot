# import nonebot
from nonebot import get_driver, permission

from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.plugin import on_startswith
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

from nonebot.permission import SUPERUSER
from src.plugins.__toolbox import checkallow

##参数
from random import choice

import os
from configs.path_config import PLUGINS_PATH,RIMAGE_PATH
THIS_PATH = os.path.join(PLUGINS_PATH,'changing')


##变猫娘
import json
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

def getcatgirl():
    from random import choice
    return choice(['100%原生态','纯天然小野猫','白猫','黑猫','小猫','大猫',
                   '猫又','猫妖','猫神','流浪猫','等待投喂の小猫',
                   '式神-橙','火焰猫燐','豪德寺三花',
                   '巧克力','香草','枫','桂','红豆','椰子','水无月时雨',
                   '小曼','小新','小露','艾尔莎',
                   'anuke','臭猫'])

change = on_startswith("魔法",endswith("魔法"),priority=6,block=True)

@change.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await change.finish()
    await bot.send(event,message="这里是茉莉的魔法实验室！目前功能：\n变猫娘：@你想变的玩家\n小天才：***\n主世界重生\n更多功能正在测试中！\n\
欢迎来一起编辑词条！词条连接：https://docs.qq.com/sheet/DVFFVbWdlalVkcHp2")

change_catgirl = on_command("变猫娘",priority=5,block=True)

@change_catgirl.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await change_catgirl.finish()
    sb = At(event.json())
    if sb == ['all']:
        await bot.send(event,message="你的法力还不够强大哦，不足以把全群人都变成猫娘的！")
    elif len(sb)>1:
        await bot.send(event,message=+"一次只能变一个！不可以贪心~")
    elif len(sb)==0 and event.is_tome():
        msg=choice(["喵~~"+MessageSegment.image(os.path.join(RIMAGE_PATH,"kimo茉莉","猫娘.jpg")),"茉莉是小狐狸！"])
        await bot.send(event,message=msg)
    elif sb == ['null'] or len(sb)==0:
        await bot.send(event,message=MessageSegment.at(event.user_id)+"挥动了法杖，一不小心把自己变成了["+getcatgirl()+"]")
    else:
        await bot.send(event,message=MessageSegment.at(event.user_id)+"使用了猫娘变化大法，把"+MessageSegment.at(sb[0])+"变成了["+getcatgirl()+"]")
    await change_catgirl.finish()
    
change = on_startswith("小天才：",priority=5,block=True)

@change.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await change.finish()
    text = str(event.message)[4:]
    sb = At(event.json())
    import random
    import pandas as pd
    data = pd.read_csv(os.path.join(THIS_PATH,'genius.csv'), index_col=0)
    if len(sb)==1:
        await bot.send(event,message="不需要@的，直接打出名字就好了！")
        await change.finish()        
    elif len(text)>10:
        await bot.send(event,message="唔~谁家的小天才名字这么长啊")
    elif len(text)==0:
        await bot.send(event,message="?")
    else:
        await bot.send(event,message=data.loc[random.choice(data.index)].text.replace('%name',text))
    await change.finish()
    
change = on_regex("^(主世界重生|投胎模拟器)$",priority=5,block=True)

@change.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'chatting')==0:
        await change.finish()
    text = str(event.message)[4:]
    import random
    import pandas as pd
    data = pd.read_csv(os.path.join(THIS_PATH,'pop_dis.csv'))
    pop_total = 7810184000
    pop_index = random.randint(0,pop_total)
    for row in range(data.shape[0]):
        pop_index -= data.loc[row]['pop']
        if pop_index<=0:
            msg = MessageSegment.reply(event.message_id)+'.'+MessageSegment.at(event.user_id)
            msg+='刷新了开局，并重生在了'+data.loc[row]['country']+' ('+str(data.loc[row,'per'])+' %)'
            await bot.send(event,message=msg)
            await change.finish()
    await change.finish()