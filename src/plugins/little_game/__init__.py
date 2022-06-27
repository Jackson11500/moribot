from nonebot import get_driver

from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

from nonebot.permission import SUPERUSER
from src.plugins.__toolbox import checkallow

global_config = get_driver().config
from configs.path_config import *

##游戏
game = on_regex("^游戏$|^小游戏$", priority=5,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'little_game')==0:
        await game.finish()
    await bot.send(event=event,message="茉莉的小游戏：\n骰子\n骰子：int(输入需要投出的范围)\n24点")
    await game.finish()

##色子
game = on_regex("(^色子$)|(^骰子$)", priority=5,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'little_game')==0:
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
    if checkallow(event,'little_game')==0:
        await game.finish()
    import random
    at = MessageSegment.at(event.user_id)
    
    saizi = str(event.message)[:2]
    if len(str(event.message))>20:
        await game.finish(at+f"扔辣么大个{saizi}干什么嘛")
    
    if str(event.message)[3]=='-' and str(event.message)[4:].isdigit():
        number = int(str(event.message)[3:])
        await game.finish(at+f"使用了一个自定义{saizi}（1~{number}）,丢出了一个{random.randint(number,0)}")
    elif not str(event.message)[3:].isdigit():
        
        msg = random.choice[f'不要乱丢奇奇怪怪的{saizi}啦~beka',f"你对{saizi}做了些什么？老实交代！",f'{saizi}只能是整数组成的懂不懂啦！']
        await game.finish(at+msg)
    else:
        number = int(str(event.message)[3:])
        if number == 0:
            await game.finish(at+f"使用了一个薛定谔{saizi},丢出了一个{random.randint(-99999999999999999999,99999999999999999999)}")
        elif number == 1:
            await game.finish(at+f"抛出了一个硬币,丢出了一个{random.randint(0,1)}")    
        else:
            await bot.send(event=event,message=at+f'使用了一个自定义{saizi}（1~{number}）,丢出了一个{random.randint(1,number)}')
        await game.finish()

##24
game = on_regex("^24点$", priority=5,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'little_game')==0:
        await game.finish()
    import random,os
    text = '随机24点：\n规则:每个数字只能且必须使用1次，只能使用+-*/及括号，并使最后结果等于24\n下列组合茉莉已经研究过并确定有解的！答不出说明你是小笨蛋\n'
    text += random.choice(open(os.path.join(PLUGINS_PATH,'little_game','24点.txt')).readlines())
    await bot.send(event=event,message=text)
    await game.finish()

##24


game = on_regex("测试",permission=SUPERUSER, priority=1,block=True)

@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'little_game')==0:
        await game.finish()
    from src.plugins.little_game.card_generator import gen_all_card
    gen_all_card()
    await game.finish()
