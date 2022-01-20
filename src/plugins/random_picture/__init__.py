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
    '小岛游':['小岛游','小屑猫','六花','小岛游六花'],
    '小恶魔':['小恶魔','小emo'],
    '小伞':['小伞','多多良小伞','多多良小鼬'],
    '水月':['水月','天幻'],
    '透明药':['透明药','chitose','klp'],

    '二次元':['二次元','二刺螈','妹子'],
    '壁纸':['壁纸','琉璃'],
    '秘封':['秘封'],
    '东方':['东方','车万'],
    '三色':['三色','三色绘恋'],
    '天使':['天使'],
    '白毛狐狸':['白毛狐狸','白狐'],
    'BlueArchive':['BA','BlueArchive','ba'],
    'AA':['AA','AscixArt'],
    '9-nine':['9-nine','9nine'],
    
    '群星':['科幻','stellaris','群星']
}

###随机图片
randomfig = on_startswith("随机", priority=11,block=True)
@randomfig.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
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



###投稿指南
figintro = on_command("投稿图片指南", priority=3,block=True)

@figintro.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'random_pic')==0:
        await randomfig.finish()
    msg = '你也想投稿图片吗？非常欢迎哦~\n\
· 如果你想添加3张及以下的图片，直接加茉莉好友然后私发给茉莉就行啦！\n\
· 但如果想一次添加3张以上的大量图片，请先自行打包成压缩包，随后直接发给lc，或者发到群里@lc或是茉莉都行！\n\
· 发送图片或梗图记得简单补充个图片说明，例如希望在什么对话下触发之类的，茉莉能明白的~\n\
· 还有还有，不要教茉莉坏坏的内容！例如涩图，脏话，哲学恶臭图等，如有发现茉莉会惩罚积分哦~毕竟大家也不会希望茉莉被气走吧~一定是这样的！\n\
· 不管怎么说，所有图片都需要经过主人审核才会加入茉莉的图包。所以....就不要想着萌混过关啦~~~'
    await figintro.finish(msg)

###库
def count_figure():
    import os
    msg_build = "茉莉已收藏了以下系列的图片！\n"
    count_fig=0
    for pic_key in pic_dict:
        count_fig_s = len(os.listdir(os.path.join(img_path,pic_key)))
        count_fig+=count_fig_s
        msg_build+="随机"+pic_dict[pic_key][0]+f'  ({count_fig_s})'+'\n'
    msg_build+='总计 '+str(count_fig)+' 个图片'
    msg_build+='\n如果你也给茉莉投稿图片，请发送\'投稿图片指南\'哦'
    return msg_build

def send_random_picture(picture_type):
    import random
    filelist = [x for x in os.listdir(os.path.join(img_path,picture_type)) if os.path.isfile(os.path.join(img_path,picture_type,x))]
    random_index = random.randrange(1,len(filelist),1)
    return os.path.join(img_path,picture_type,filelist[random_index]),random_index,len(filelist)
    
    
    
    
    
    
