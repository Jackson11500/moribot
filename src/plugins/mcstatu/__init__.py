# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command
from nonebot.rule import endswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment

from configs.path_config import PLUGINS_PATH
import os
THIS_PATH = os.path.join(PLUGINS_PATH,'mcstatu')

from mcstatus.server import MinecraftServer
###服务器状态
mc_status = on_command("mc服状态",rule=endswith("mc服状态"), priority=5,block=True)
@mc_status.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not str(event.group_id) in ['718017633','931790051','180707407']:
        await mc_status.finish()
    
    server = MinecraftServer.lookup("mega.mcla.fun:22544")
    msg = "winecraft mc服务器"
    #msg += "查询服务器："+address
    msg += "\n服务器延迟："+str(int(server.ping()))+" ms"
    playercount = server.status().players.online
    if playercount ==0:
        msg += '\n'+"服务器现在没有人呢~"
    else:
        msg += '\n'+"服务器在线人数："+str(server.status().players.online)
        msg += '\n'+"他们是："
        playerlist = tuple(player.name for player in server.status().players.sample)
        for i in range(len(playerlist)):
            msg += '\n'+playerlist[i]
    await bot.send(event=event,message=MessageSegment.reply(event.message_id)+msg)
    await mc_status.finish()
    
    