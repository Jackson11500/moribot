# import nonebot


from nonebot import get_driver

from .config import Config

from nonebot import on_command,on_regex
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())


###
morisama = on_regex("^茉莉酱!$|^茉莉酱！$", priority=2,block=True)

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    text = "主人找我有什么事呢？\n\
我已经在努力学习了！可没有摸鱼呢\n\
已支持地功能大类：\n\
* 实用资料\n\
* 图片管家（随机图片...）\n\
* 个人信息管理（签到...）\n\
茉莉现在和以前不同啦，会和大家进行更多的互动，并且可以通过模式设置来调整哦\n\
输入茉莉模式查询|修改当前模式！"
    await morisama.finish(text)


