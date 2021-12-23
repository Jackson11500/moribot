# import nonebot


from nonebot import get_driver

from .config import Config

from nonebot import on_command
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())


az = on_command("az", rule=to_me(), priority=5,block=True)

@az.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    from random import choice
    text = choice(['啊这','别az了，你只会az吗？','你又在az了，休息一下好不好'])
    await az.finish(text)
    

