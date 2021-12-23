# import nonebot


from nonebot import get_driver

from .config import Config

from nonebot import on_command
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())

###
mori = on_command("茉莉酱", rule=startswith('茉莉酱'), priority=7,block=True)

@mori.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await mori.finish("是在找我吗？还在学习中哦~~会尽快与大家见面的！一定是这样的！")

###
morisama = on_command("茉莉酱！", priority=2,block=True)

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    text = "主人找我有什么事呢？\n茉莉正在习惯新环境，期待与大家见面哦~~\n"\
        +"目前进度：学习基础语法中......"
    await morisama.finish(text)

###
hello = on_command("你好", rule=to_me(), priority=5,block=True)

@hello.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await hello.finish("欢迎回来")



    

