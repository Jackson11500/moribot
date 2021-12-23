# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

## 参数
accept_group = [180707407,931790051,697981760,904318344,740835470]
img_path = "file:///D://QQ//Bot//mdt-数据//计算向//"


###实用资料
reslist = on_command("实用资料", priority=3,block=True)

@reslist.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = '茉莉的实用资料列表：\n\
--蓝图档案馆\n\
--资料导航站\n\
--逻辑大全\n\
--颜色列表'
    await reslist.finish(msg)

###蓝图档案馆
bparchive = on_command("蓝图档案馆", priority=3,block=True)

@bparchive.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = '欢迎来到mindustry蓝图档案馆\n\
我们致力于收藏所有同类蓝图中最好的蓝图！\n\
蓝图档案馆：https://docs.qq.com/sheet/DVHNoS3lIcm1NbFFS\n\
欢迎每位蓝图人前往优化蓝图！完美蓝图档案馆需要每个蓝图人的努力！\n\
由于有坏孩子不遵守档案馆使用规则，现仅部分玩家开放编辑权限。如果您发现无档案馆编辑权限，可以先前往蓝图审查局上传蓝图，通过后即可归档。优质蓝图作者即可获得主文档编辑权限\n\
蓝图审查局：https://docs.qq.com/sheet/DVGRjTFNadXJYcHZY\n'
    await bparchive.finish(msg)

###资料导航站
resarchive = on_command("资料导航站", priority=3,block=True)

@resarchive.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = '欢迎来到mindustry资料导航站\n\
我们致力于收集mdt所有群组|平台|资料站！\n\
资料导航站：https://docs.qq.com/sheet/DVEVob2xrcVBzQk5R\n\
资料导航站对所有玩家完全开放编辑，欢迎各位玩家前往补充资料！'
    await resarchive.finish(msg)

###逻辑大全
res_logic = on_command("逻辑大全", priority=3,block=True)

@res_logic.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message="是小撒姐姐做的哦~非常的实用呢\n"+MessageSegment.image(file = img_path+"逻辑介绍.jfif"))
    await res_logic.finish()

###颜色列表
res_color = on_command("颜色列表", priority=3,block=True)

@res_color.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event=event,message="Way_Zer调出来的！\n"+MessageSegment.image(file = img_path+"搞颜色.png"))
    await res_color.finish()
'''
#randomfig = on_startswith("", priority=3,block=True)
@randomfig.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    pic_type = str(event.message)[2:]
    if pic_type == "图片":
        msg_build = count_figure()
        await randomfig.finish(msg_build)
        
    for pic_key in pic_dict:
        if pic_type in pic_dict[pic_key]:
            pic,index,total = send_random_picture(pic_key)
            await bot.send(event=event,message=event.message+f": {index}/{total}\n"+MessageSegment.image(file = "file:///"+pic))
            await randomfig.finish()
    
    await randomfig.finish("？")
    
###投稿指南
###签到
#user_signin = on_command("投稿图片指南", priority=3,block=True)

@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = '你也想投稿图片吗？非常欢迎哦~\n\
· 如果你想添加3张及以下的图片，直接加茉莉好友然后私发给茉莉就行啦！\n\
· 但如果想一次添加3张以上的大量图片，请先自行打包成压缩包，随后直接发给lc，或者发到群里@lc或是茉莉都行！\n\
· 发送图片或梗图记得简单补充个图片说明，例如希望在什么对话下触发之类的，茉莉能明白的~\n\
· 还有还有，不要教茉莉坏坏的内容！例如涩图，脏话，哲学恶臭图等，如有发现茉莉会惩罚积分哦~毕竟大家也不会希望茉莉被气走吧~一定是这样的！\n\
· 不管怎么说，所有图片都需要经过主人审核才会加入茉莉的图包。所以....就不要想着萌混过关啦~~~'
    await randomfig.finish(msg)

def count_figure():
    import os
    msg_build = "茉莉已收藏了以下系列的图片！\n"
    count_fig=0
    for pic_key in pic_dict:
        ran_img_path = "D://QQ//Bot//定向回复//随机包//"+pic_key
        count_fig_s = len(os.listdir(ran_img_path))
        count_fig+=count_fig_s
        msg_build+="随机"+pic_dict[pic_key][0]+f'  ({count_fig_s})'+'\n'
        
    msg_build+='总计 '+str(count_fig)+' 个图片'
    msg_build+='\n如果你也给茉莉投稿图片，请发送\'投稿图片指南\'哦'
    return msg_build

def send_random_picture(picture_type):
    ran_img_path = "D://QQ//Bot//定向回复//随机包//"+picture_type
    import os,random
    filelist = [x for x in os.listdir(ran_img_path) if os.path.isfile(ran_img_path+"//"+ x)]
    random_index = random.randrange(1,len(filelist),1)
    return ran_img_path+"//"+ filelist[random_index],random_index,len(filelist)
    
'''
    
    
    
    
