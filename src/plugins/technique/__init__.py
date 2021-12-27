# import nonebot
from nonebot import get_driver
from numpy import source

global_config = get_driver().config

from nonebot import on_command,on_startswith,on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import isallow

## 参数
img_path = "file:///D://QQ//Bot//mdt-数据//计算向//"


###实用资料
reslist = on_regex("^实用资料$", priority=3,block=True)

@reslist.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    msg = '茉莉的实用资料列表：\n\
--蓝图档案馆\n\
--资料导航站\n\
--逻辑大全\n\
--颜色列表'
    await reslist.finish(msg)

###蓝图档案馆
bparchive = on_regex("^蓝图档案馆$", priority=3,block=True)

@bparchive.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    msg = '欢迎来到mindustry蓝图档案馆\n\
我们致力于收藏所有同类蓝图中最好的蓝图！\n\
蓝图档案馆：https://docs.qq.com/sheet/DVHNoS3lIcm1NbFFS\n\
欢迎每位蓝图人前往优化蓝图！完美蓝图档案馆需要每个蓝图人的努力！\n\
由于有坏孩子不遵守档案馆使用规则，现仅部分玩家开放编辑权限。如果您发现无档案馆编辑权限，可以先前往蓝图审查局上传蓝图，通过后即可归档。优质蓝图作者即可获得主文档编辑权限\n\
蓝图审查局：https://docs.qq.com/sheet/DVGRjTFNadXJYcHZY\n'
    await bparchive.finish(msg)

###资料导航站
resarchive = on_regex("^资料导航站$", priority=3,block=True)

@resarchive.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    msg = '欢迎来到mindustry资料导航站\n\
我们致力于收集mdt所有群组|平台|资料站！\n\
资料导航站：https://docs.qq.com/sheet/DVEVob2xrcVBzQk5R\n\
资料导航站对所有玩家完全开放编辑，欢迎各位玩家前往补充资料！'
    await resarchive.finish(msg)

###逻辑大全
res_logic = on_regex("^逻辑大全$", priority=3,block=True)

@res_logic.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    await bot.send(event=event,message="是小撒姐姐做的哦~非常的实用呢\n"+MessageSegment.image(file = img_path+"逻辑介绍.jfif"))
    await res_logic.finish()

###颜色列表
res_color = on_regex("(^颜色列表$)|(^颜色大全$)", priority=3,block=True)

@res_color.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    await bot.send(event=event,message="Way_Zer调出来的！\n"+MessageSegment.image(file = img_path+"搞颜色.png"))
    await res_color.finish()
    

def get_forward_msg(bot,event,source_file):
    source = ""
    f = open(img_path+"type//"+source_file)
    line = f.readline()
    while line:
        if len(line)>=5:
            source+=line
        line = f.readline()
    f.close()
    
    msg_list = []
    sender = {
    "type": "node",
    "data": {
        "id":str(event.message_id)
    },
    }
    msg_list.append(sender)
    source_data = {
    "type": "node",
    "data": {
        "name": f"无所不知茉莉酱",
        "uin": f"{bot.self_id}",
        "content": f"下面茉莉发送的是{source_file}的源码",
    },
    }
    msg_list.append(source_data)
    data = {
    "type": "node",
    "data": {
        "name": f"无所不知茉莉酱",
        "uin": f"{bot.self_id}",
        "content": source,
    },
    }
    msg_list.append(data)
    return msg_list

###每日重启
source_recode = on_regex("^源码重置$", priority=1, permission=SUPERUSER,block=True)

@source_recode.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.technique.source as source
    source.process_code()
    await bot.send(event=event,message="源码已重置！")
    await source_recode.finish("")

###源码查询
img_path = "D://QQ//Bot//mdt-数据//"
source_code = on_command("源码：",aliases={"source=","源码:","source ="},priority=5,block=True)
@source_code.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,1):
        await reslist.finish()
    source_file =  str(event.get_message()).lower()
    import os
    if os.path.exists(img_path+"type//"+source_file):
        await bot.send_group_forward_msg(group_id=event.group_id,messages = get_forward_msg(bot,event,source_file))
    else:
        await bot.send(event = event, message = "茉莉找不到这个源码！会不会是你输错了呢？")
    await source_code.finish()
    

    