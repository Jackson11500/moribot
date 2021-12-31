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
someonesay = on_startswith("有人说", priority=3,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    if len(str(event.message))>10:
        await someonesay.finish()
    await bot.send(event=event,message="茉莉的名人名言系列(需要加上中文冒号哦)~~目前支持\n\鲁迅说：\n\追杀图：")
    await someonesay.finish()
    

###自定义图
luxunsay = on_startswith("鲁迅说：", priority=3,block=True)
@luxunsay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await luxunsay.finish()
    says = str(event.message)[4:]
    if len(says)>40:
        await luxunsay.finish('太长了，鲁迅说不完...')
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    luxun_fig = Image.open(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\luxun.jpg')
    msjh_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, luxun_fig.width // 15)
    for index in range(len(says)//10+1):
        ImageDraw.Draw(luxun_fig).text(xy=(int(luxun_fig.width/2), int(luxun_fig.height*2/3)+index*30),
                                        text=says[int(index*10):int(min(len(says),index*10+9)+1)], font=msjh_text_font, align='center',anchor='mm',
                                        fill=(256, 256, 256))
    ImageDraw.Draw(luxun_fig).text(xy=(int(luxun_fig.width/10*9), int(luxun_fig.height/10*9)),
                                    text='——鲁迅', font=msjh_text_font, align='center',anchor='rb',
                                    fill=(256, 256, 256))
    luxun_fig.save(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_luxun.jpg', 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_luxun.jpg'))
    await luxunsay.finish()    
        
###自定义图
someonesay = on_startswith("追杀图：", priority=3,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[4:]
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    someone_fig = Image.open(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\追杀.jpg')
    msjh_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, someone_fig.width // 15)
    text_width, text_height = msjh_text_font.getsize(says)  
    if text_width>=someone_fig.width/3:
        await someonesay.finish('字数超出限制了的说~')
    ImageDraw.Draw(someone_fig).text(xy=(int(someone_fig.width/4), int(someone_fig.height/15*14)),
                                    text=says, font=msjh_text_font, align='center',anchor='mm',
                                    fill=(0, 0, 0))
    someone_fig.save(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_fig.jpg', 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_fig.jpg'))
    await someonesay.finish()   
    
    
    
'''
someonesay = on_startswith("nobeta：", priority=3,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[7:]
    
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import os
    someone_fig = Image.open(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\nobeta.jpg')
    font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'ruanmeng.ttf'))
    font = ImageFont.truetype(font_path, someone_fig.width // 10)
    text_width, text_height = font.getsize(says)  
    if text_width>=someone_fig.width/2:
        await someonesay.finish('字数超出限制了的说~')
        
    txt=Image.new('L', (200,200))
    d = ImageDraw.Draw(txt)
    d.text(xy=(0,0),text=says, font=font, align='left',anchor='lt',fill=255)
    w=txt.rotate(13,  expand=1)
    someone_fig = someone_fig.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (int(someone_fig.width/2),int(someone_fig.height/2)),  w)
    someone_fig.save(os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_fig.jpg', 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.getcwd()+'\\src\\plugins\\someone_say\\resources\\ls_file\\ls_fig.jpg'))
    await someonesay.finish()   
'''