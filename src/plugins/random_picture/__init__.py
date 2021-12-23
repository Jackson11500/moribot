# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

## 参数
accept_group = [180707407,931790051,697981760]

###
moritest = on_startswith("随机", priority=3, permission=SUPERUSER,block=True)
img_path = "file:///D://QQ//Bot//定向回复//随机包"

pic_dict = {
    'cloverday':['lc','CloverDay'],
    '高血压':['高血压'],
    'kimo':['狐狸','茉莉','kimo','kimo酱']
}

@moritest.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if event.group_id not in accept_group:
        return 0
    pic_type = str(event.message)[2:]
    
    for pic_key in pic_dict:
        if pic_type in pic_dict[pic_key]:
            pic,index,total = send_random_picture(pic_key)
            await bot.send(event=event,message=event.message+f":{index}/{total}\n"+pic+MessageSegment.image(file = "file:///"+pic))
            await moritest.finish()
    
    await moritest.finish()
    
    
    
def send_random_picture(picture_type):
    ran_img_path = "D://QQ//Bot//定向回复//随机包//"+picture_type
    import os,random
    filelist = [x for x in os.listdir(ran_img_path) if os.path.isfile(ran_img_path+"//"+ x)]
    random_index = random.randrange(1,len(filelist),1)
    return ran_img_path+"//"+ filelist[random_index],random_index,len(filelist)
    
    
    
    
    
    
