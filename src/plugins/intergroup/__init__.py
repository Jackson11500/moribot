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

from nonebot.adapters.cqhttp import GROUP_ADMIN, GROUP_OWNER

from configs.path_config import PLUGINS_PATH

game = on_regex("^群组状态$", priority=5,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message="这一部分茉莉会作为各个群组沟通的桥梁！")
    await game.finish()

set_status = on_command("群组状态设置：",permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,priority=5,block=True)
@set_status.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    command = str(event.message).split('：')
    import pandas as pd
    import os
    group_status=pd.read_csv(os.path.join(PLUGINS_PATH,'group_status.csv'), index_col=0)
    if command[0] not in ['group_name','intro','chatting','intergroup','little_game','mdt','random_pic','someone_say','technique','user']:
        await set_status.finish('茉莉无法识别此命令，请检测拼写或格式！')
    
    if len(command[1])==0:
            await set_status.finish('茉莉无法识别此命令，请检测拼写或格式！')
            
    if len(command[1])==20:
            await set_status.finish('字符太长啦~~~不可以输入这么多字的，是故意的还是格式不对呢？')              
    
    if command[0] != 'group_name' and command[0] != 'intro':
        if command[1] != '0' and command[1] != '1':
            await set_status.finish('您只能选择0(关闭)或1(开启)')
        group_status.loc[str(event.group_id),command[0]] = int(command[1])
        group_status.to_csv(os.path.join(PLUGINS_PATH,'group_status.csv'))
        await set_status.finish('状态设置成功！')
            
    group_status.loc[str(event.group_id),command[0]] = command[1]
    group_status.to_csv(os.path.join(PLUGINS_PATH,'group_status.csv'))
    await set_status.finish('群组属性设置成功！')

