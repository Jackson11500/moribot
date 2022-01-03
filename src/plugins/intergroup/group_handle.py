import pandas as pd
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from typing import Union
from nonebot.adapters.cqhttp.message import Message, MessageSegment

async def draw_group_status(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    查询并绘制群组状态
    '''
    