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
from src.plugins.__toolbox import isallow

##参数
from random import choice

img_path = "file:///D://QQ//Bot//定向回复//"


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

change_catgirl = on_command("变猫娘",priority=3,block=True)

@change_catgirl.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event.group_id,2):
        await change_catgirl.finish()
    sb = At(event.json())
    if sb == ['all']:
        await bot.send(event,message="你的法力还不够强大哦，不足以把全群人都变成猫娘的！")
    elif len(sb)>1:
        await bot.send(event,message=+"一次只能变一个！不可以贪心~")
    elif len(sb)==0 and event.is_tome():
        msg=choice(["喵~~"+MessageSegment.image(img_path+"kimo茉莉//猫娘.jpg"),"茉莉是小狐狸！"])
        await bot.send(event,message=msg)
    elif sb == ['null'] or len(sb)==0:
        await bot.send(event,message=MessageSegment.at(event.user_id)+"挥动了法杖，一不小心把自己变成了["+getcatgirl()+"]")
    else:
        await bot.send(event,message=MessageSegment.at(event.user_id)+"使用了猫娘变化大法，把"+MessageSegment.at(sb[0])+"变成了["+getcatgirl()+"]")
    await change_catgirl.finish()