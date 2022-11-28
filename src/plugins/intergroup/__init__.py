# import nonebot


from nonebot import get_driver, permission


from nonebot import on_regex,on_command,on_notice,on_message
from nonebot.plugin import on_startswith
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.onebot.v11 import Bot,Event,MessageSegment,GroupMessageEvent

from nonebot.permission import SUPERUSER
from src.plugins.__toolbox import checkallow

global_config = get_driver().config
from configs.path_config import PLUGINS_PATH

from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER

game = on_command("群组服务",priority=5,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if len(str(event.message))>0:
        await game.finish()
    msg='群组服务命令列表：\n群组状态[用于查看群组开放的功能]\n群组状态设置：[用于调整群组开放的功能，仅管理]\n传信：[用于向其他群发送一个信息]'
    await bot.send(event=event,message=msg)
    await game.finish()

game = on_command("群组状态",priority=5,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if len(str(event.message))>0:
        await game.finish()
    import src.plugins.intergroup.group_handle as gh
    text = await gh.draw_group_status(bot=bot, event=event, state=state)
    await bot.send(event=event,message=MessageSegment.reply(event.message_id)+MessageSegment.image(file = "file:///"+text))
    await game.finish()

game = on_command("群组状态设置",rule=endswith("群组状态设置"),permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,priority=6,block=True)
@game.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if len(str(event.message))>0:
        await game.finish()
    msg='群主|群管限定指令、用于调整群组服务状态\n格式：\n群组状态设置：[状态名]：[设置项]\n\
举例：\n群组状态设置：intro：一个好玩的群\n群组状态设置：random_pic：0\n\
状态名可以通过[群组状态]指令查询\n其中intro与group_name可以输入20字以下字符，其他的输入0或1（分别表示关闭、开启）'
    await bot.send(event=event,message=msg)
    await game.finish()

set_status = on_startswith("群组状态设置：",permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,priority=7,block=True)
@set_status.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    command = str(event.message).split('：')
    import pandas as pd
    import os
    group_status=pd.read_csv(os.path.join(PLUGINS_PATH,'group_status.csv'), index_col=0)
    if command[0] not in ['group_name','intro','chatting','intergroup','little_game','mdt','random_pic','someone_say','technique','user']:
        await set_status.finish()
    
    if len(command[1])==0:
            await set_status.finish('茉莉无法识别此命令，请检测拼写或格式！\n群组状态设置：状态名：更改内容')
            
    if len(command[1])==20:
            await set_status.finish('字符太长啦~~~不可以输入这么多字的，是故意的还是格式不对呢？\n群组状态设置：状态名：更改内容')              
        #'茉莉无法识别此命令，请检测拼写或格式！\n群组状态设置：状态名：更改内容'
    if command[0] != 'group_name' and command[0] != 'intro':
        if command[1] != '0' and command[1] != '1':
            await set_status.finish('只能输入状态为0或1(分别表示关闭和开启)!')
        group_status.loc[str(event.group_id),command[0]] = int(command[1])
        group_status.to_csv(os.path.join(PLUGINS_PATH,'group_status.csv'))
        await set_status.finish('状态设置成功！')
            
    group_status.loc[str(event.group_id),command[0]] = command[1]
    group_status.to_csv(os.path.join(PLUGINS_PATH,'group_status.csv'))
    await set_status.finish('群组属性设置成功！')

intergroup = on_command("传信",rule = endswith('传信'),priority=8,block=True)
@intergroup.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'intergroup')==0:
        await intergroup.finish()
    await bot.send(event=event,message='传信--允许向其他群组发送信息\n只有开启群间交互功能的群才能使用和接受\n发送格式：\n传信：群id：内容\n暂仅支持纯文本，信纸价格2|4|0|0，所需等级：3')
    await intergroup.finish()    

intergroup = on_command("传信：",priority=8,block=True)

@intergroup.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'intergroup')==0:
        await intergroup.finish()

    command = str(event.message).split('：')
    group_id = command[0]
    
    if not group_id.isdigit:
        await intergroup.finish('你们这是什么群啊，根本就不是正常的群号好嘛，检查好了再输入！')
    from src.plugins.__toolbox import checkallow_g,get_proporties
    if checkallow_g(int(group_id),'intergroup') == -1:
        await bot.send(event=event,message='这个群不在茉莉的服务范围！\n（茉莉不在此群）')
        await intergroup.finish()
        return 0
    elif checkallow_g(int(group_id),'intergroup') == 0:
        await intergroup.finish('收件人拒收了邮件!可能是不希望有人打扰吧\n（目标群关闭了群间信息交互功能）')
    elif int(group_id) == int(event.group_id):
        await intergroup.finish('禁止原地tp')
    else:
        if len(command[1])>200:
            await intergroup.finish('不可以在其他群刷屏的！\n（信息过长）')
        from src.plugins.user.utils import check_service
        if check_service(int(event.user_id),'传信')==99:
            group_name = get_proporties(int(event.group_id),'group_name')
            msg = f'群间消息：你收到一条来自{group_name}的由@{event.user_id}发送的信息，TA说：\n'
            msg += command[1]
            msg += f'\n可以通过传信来回复消息！'
            await bot.send_group_msg(group_id=int(group_id), message=msg)
            await bot.send(event=event,message=MessageSegment.reply(event.message_id)+"信件已送达对方！")
            await intergroup.finish()
        else:
            await intergroup.finish('呜呜，发送失败了~可能是你等级不够或者没有铜铅买信纸！')
