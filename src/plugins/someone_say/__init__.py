from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_startswith
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import isallow

RESOURCES_PATH = 'D://QQ//Bot//nonebot//moribot//resources//'

###自定义图
luxunsay = on_startswith("鲁迅说", priority=3,block=True)
@luxunsay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await luxunsay.finish()
    says = str(event.message)[3:]
    if len(says)>40:
        await luxunsay.finish('太长了，鲁迅说不完...')
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    luxun_fig = Image.open(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\luxun.jpg')
    
    msjh_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, luxun_fig.width // 15)

    #ImageDraw.Draw(luxun_fig).text(xy=(int(luxun_fig.width/2), int(luxun_fig.width*2/3)),
    #                                text=says[0:3], font=msjh_text_font, align='middle',anchor='mm',
    #                                fill=(256, 256, 256))

    for index in range(len(says)//10+1):
        ImageDraw.Draw(luxun_fig).text(xy=(int(luxun_fig.width/2), int(luxun_fig.height*2/3)+index*30),
                                        text=says[int(index*10):int(min(len(says),index*10+9))], font=msjh_text_font, align='center',anchor='mm',
                                        fill=(256, 256, 256))

    for index in range(len(says)//10+1):
        ImageDraw.Draw(luxun_fig).text(xy=(int(luxun_fig.width/10*9), int(luxun_fig.height/10*9)),
                                        text='——周树人', font=msjh_text_font, align='center',anchor='rb',
                                        fill=(256, 256, 256))    

    luxun_fig.save(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_luxun.jpg', 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_luxun.jpg'))
    await luxunsay.finish()    
        
    
    