# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.adapters.cqhttp import Bot,Event,MessageSegment


from src.plugins.__toolbox import checkallow

from configs.path_config import RIMAGE_PATH
import os
###
img_path = os.path.join(RIMAGE_PATH,'随机包')

pic_dict = {
    'kimo':['茉莉','狐狸','kimo','kimo酱'],
    
    '高血压':['高血压'],
    '梗图':['梗图'],
    
    'shizuku':['小汤圆','shizuku','猫娘'],
    '帕秋莉':['emoji','帕秋莉'],
    'cloverday':['lc','cloverday'],
    '燐猫':['工业2','mi2','燐猫','火焰猫燐'],
    '乃爱':['carrot','萝卜','乃爱'],
    '大猫':['大猫'],
    '小鸟游':['小鸟游','小屑猫','六花','小鸟游六花'],
    '小恶魔':['小恶魔','小emo'],
    '小伞':['小伞','多多良小伞','多多良小鼬'],
    '水月':['水月','天幻'],
    '透明药':['透明药','chitose','klp'],
    'furry':['furry','福瑞','法仆塔'],
    '西瓜':['西瓜','yaddr','yaddrx2','有案底的人'],
    '石油':['石油'],
    '雨2':['雨2','ipecac','雨中冒险2','ror2'],
    
    'capoo':['capoo','咖波'],
    '秘封':['秘封'],
    '东方':['东方','车万'],
    '三色':['三色','三色绘恋'],
    '天使':['天使'],
    '白毛狐狸':['白毛狐狸','白狐'],
    '妃爱':['妃爱','妹妹'],
    '小苏茜':['小苏茜'],
    'BlueArchive':['BA','BlueArchive','ba'],
    'AA':['AA','AscixArt'],
    '9-nine':['9-nine','9nine'],
    '群星':['科幻','stellaris','群星'],
    'bg':['osu','bg','osu!'],

    '二次元':['二次元','二刺螈','妹子'],
    '壁纸':['壁纸','琉璃'],
    #'xp':['xp']
}

###随机图片
randomfig = on_startswith("随机", priority=11,block=True)
@randomfig.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    #await randomfig.finish("特殊时期，功能已关闭，请过两天再试哦~~")
    if checkallow(event,'random_pic')==0:
        await randomfig.finish()
    from src.plugins.user.utils import check_service
    if check_service(event.user_id,'图片')!=99:
        await randomfig.finish("你的铜不够制作图片，炼点再回来吧！\n(可能是没注册或是铜不够)")
        
    pic_type = str(event.message)[2:]
    if len(pic_type)>7:
        await randomfig.finish()
    if pic_type == "图片":
        msg_build = count_figure()
        await randomfig.finish(msg_build)
    for pic_key in pic_dict:
        if pic_type in pic_dict[pic_key]:
            pic,index,total = send_random_picture(pic_key)
            await bot.send(event=event,message=event.message+f": {index}/{total}\n"+MessageSegment.image(file = "file:///"+pic))
            await randomfig.finish()
    await randomfig.finish("？")

###随机图片
randomfig = on_startswith("图包-随机", priority=10,block=True)
@randomfig.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    #await randomfig.finish("特殊时期，功能已关闭，请过两天再试哦~~")
    if checkallow(event,'random_pic')==0:
        await randomfig.finish()
    from src.plugins.user.utils import check_service
    if check_service(event.user_id,'图包')!=99:
        await randomfig.finish("你的铜不够制作图片，炼点再回来吧！\n(可能是没注册或是铜不够)")
        
    pic_type = str(event.message)[5:]
    if len(pic_type)>7:
        await randomfig.finish()
    if pic_type == "图片":
        msg_build = count_figure()
        await randomfig.finish(msg_build)
    
    for pic_key in pic_dict:
        if pic_type in pic_dict[pic_key]:
            pic,index,total = send_random_picture(pic_key)
            
            msg_list = []
            main = {
            "type": "node",
            "data": {
                "name": f"无情的发图茉莉姬",
                "uin": f"{bot.self_id}",
                "content": f"下面茉莉发送的是：随机{pic_type}，这个图包中总共含有{total}张图",
            },
            }
            msg_list.append(main)
            for i in range(10):
                pic,index,total = send_random_picture(pic_key)
                main = {
                "type": "node",
                "data": {
                    "name": f"随机{pic_type}：{index}",
                    "uin": f"{bot.self_id}",
                    "content": MessageSegment.image(file = "file:///"+pic),
                },
                }
                msg_list.append(main)
            await bot.send_group_forward_msg(group_id=event.group_id,messages = msg_list)
            await randomfig.finish()
    await randomfig.finish(f"茉莉没有收藏{pic_type}的图片，可以加茉莉的画展群提交图包！[873413448]")

###投稿指南
figintro = on_command("投稿图片指南", priority=3,block=True)

@figintro.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'random_pic')==0:
        await randomfig.finish()
    msg = '你也想投稿图片吗？非常欢迎哦~\n\
· 如果是少量3张以内的图片，直接@lc即可哦(什么？lc是谁？那可能说明她不希望在这个群接受少量图片的投稿哦)\n\
· 但如果想一次添加3张以上的大量图片，请先自行打包成压缩包，直接发给lc，或者加入茉莉的画展群[873413448]提交图片哦！\n\
· 发送图片或梗图记得简单补充个图片说明，例如希望在什么对话下触发之类的，茉莉能明白的~\n\
· 还有还有，不要教茉莉坏坏的内容！例如涩图，脏话，哲学恶臭图等，如有发现茉莉会惩罚积分哦~毕竟大家也不会希望茉莉被气走吧~一定是这样的！\n\
· 不管怎么说，所有图片都需要经过主人审核才会加入茉莉的图包。所以....就不要想着萌混过关啦~~~'
    await figintro.finish(msg)

###库
def count_figure():
    import os
    msg_build = "发送单张图片直接输入'随机**'即可，发送大量图片请使用'图包-随机**'以减少刷屏\n"
    count_fig=0
    for pic_key in pic_dict:
        count_fig_s = len(os.listdir(os.path.join(img_path,pic_key)))
        count_fig+=count_fig_s
        msg_build+="随机"+pic_dict[pic_key][0]+f'  ({count_fig_s})'+'\n'
    msg_build+='总计 '+str(count_fig)+' 个图片'
    msg_build+='\n如果你也想给茉莉投稿图片，请发送\'投稿图片指南\'哦'
    return msg_build

def send_random_picture(picture_type):
    import random
    filelist = [x for x in os.listdir(os.path.join(img_path,picture_type)) if os.path.isfile(os.path.join(img_path,picture_type,x))]
    random_index = random.randrange(1,len(filelist),1)
    return os.path.join(img_path,picture_type,filelist[random_index]),random_index,len(filelist)
    
    
    
    
    
    
