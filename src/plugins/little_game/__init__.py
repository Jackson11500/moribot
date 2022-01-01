# import nonebot


from nonebot import get_driver, permission


from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.rule import to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

from nonebot.permission import SUPERUSER
from src.plugins.__toolbox import isallow

global_config = get_driver().config
from configs.path_config import PLUGINS_PATH

##游戏
game = on_regex("^游戏$|^小游戏$", priority=5,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await game.finish()
    await bot.send(event=event,message="茉莉的小游戏：\n骰子\n骰子：int(输入需要投出的范围)\n24点")
    await game.finish()

##色子
game = on_regex("(^色子$)|(^骰子$)", priority=5,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await game.finish()
    import random
    at = MessageSegment.at(event.user_id)
    text = f'使用了一个{str(event.message)[:]},丢出了一个{random.randint(1,6)}'
    await bot.send(event=event,message=at+text)
    await game.finish()

##色子
game = on_regex("(^色子：)|(^骰子：)", priority=5,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await game.finish()
    import random
    at = MessageSegment.at(event.user_id)
    await bot.send(event=event,message=at+f'使用了一个自定义{str(event.message)[:2]}（1~{int(str(event.message)[3:])}）,丢出了一个{random.randint(1,int(str(event.message)[3:]))}')
    await game.finish()

##24
game = on_regex("^24点$", priority=5,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await game.finish()
    import random,os
    text = '随机24点：\n规则:每个数字只能且必须使用1次，只能使用+-*/及括号，并使最后结果等于24\n下列组合茉莉已经研究过并确定有解的！答不出说明你是小笨蛋\n'
    text += random.choice(open(os.path.join(PLUGINS_PATH,'little_game','24点.txt')).readlines())
    await bot.send(event=event,message=text)
    await game.finish()