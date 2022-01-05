# import nonebot


from nonebot import get_driver

from .config import Config

from nonebot import on_command,on_regex
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())

from src.plugins.__toolbox import isallow

###
morisama = on_regex("(^茉莉酱$)|(^茉莉酱!$)|(^茉莉酱！$)", priority=2,block=True)

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    text = "主人找我有什么事呢？\n\
我已经在努力学习了！可没有摸鱼呢\n\
输入以下命令以查询相关功能大类：\n\
* 实用资料\n\
* 随机图片\n\
* 签到\n\
* 源码：mono\n\
* 有人说\n\
* 小游戏\n\
* 群组服务\n\
* 交易\n\
如果命令没反应，可能是茉莉暂时离开或者未开启服务哦，请确认茉莉当前状态。\n\
输入'群组服务'以查看模式，管理或群主可输入'群组状态设置'来进行调整！"
    await morisama.finish(text)

##
morisama = on_command("茉莉状态",endswith('茉莉状态'), priority=2,block=True)
modename = {0:"冬眠",1:"打盹",2:"游玩",3:"发情"}
modedes = {0:"除了呼唤与修改状态指定外忽视一切指令",1:"仅会接受主动呼唤相关的内容",2:"会积极主动参与聊天中",3:"开放隐藏对话"}

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import numpy as np
    mode = np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()[event.group_id]
    await bot.send(event=event,message=f"茉莉当前状态：[{mode}]{modename[mode]}中...\n({modedes[mode]})\n如果想切换模式，请输入：\n茉莉状态切换 id\n如果想了解各状态功能，请输入：\n茉莉状态说明")

    await morisama.finish()

##状态说明
morisama = on_regex("^茉莉状态说明$", priority=2,block=True)

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message="茉莉当前共有4种状态：\n\
冬眠状态[0]：除了呼唤与修改状态指定外忽视一切指令\n\
打盹状态[1]：仅会接受主动呼唤相关的内容\n\
游玩状态[2]：会积极主动参与聊天中\n\
？未知状态[3]：暂时不开放哦")
    await morisama.finish()

##状态切换
morisama = on_command("茉莉状态切换",aliases={'茉莉状态设置'}, priority=2,block=True)

@morisama.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    from random import choice
    import numpy as np
    group_status = np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()
    mode = group_status[event.group_id]
    try:
        switch_mode = int(str(event.get_message()).split()[-1][-1])
    except TypeError:
        await bot.send(event=event,message=choice["茉莉无法识别你输入的信息!","说人话！","？","不按要求输入的话茉莉是不会理你的"])
        await morisama.finish()
    
    if switch_mode == mode:
        await bot.send(event=event,message=f"茉莉已经是这个状态啦！你还想怎样~~\n({modedes[switch_mode]})")
        await morisama.finish()
    
    if switch_mode == 3 and not event.user_id == 853330464:
        await bot.send(event=event,message=f"有些状态是不可能公开的！<羞羞~~>")
        await morisama.finish()
        
    if switch_mode >=4:
        await bot.send(event=event,message=f"新的状态还在学习中哦~~")
        await morisama.finish()

    if switch_mode <0:
        await bot.send(event=event,message=choice["baka，再乱输我就不理你了，哼！","冬眠已经是最低功耗态啦~","呜呜，你是想让茉莉永远消失嘛~"])
        await morisama.finish()    
    
    #成功切换
    group_status[event.group_id] = switch_mode
    np.save('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',group_status)
    if switch_mode>=2:
        await bot.set_group_card(group_id = event.group_id,user_id=bot.self_id,card='小狐狸茉莉')
    else:
        await bot.set_group_card(group_id = event.group_id,user_id=bot.self_id,card='小狐狸茉莉 '+str(modename[switch_mode])+'中...')
    await bot.send(event=event,message=f"茉莉已成功切换至：[{switch_mode}]{modename[switch_mode]}中...\n({modedes[switch_mode]})")
    await morisama.finish()
