from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_startswith
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import isallow

from configs.path_config import PLUGINS_PATH,FONT_PATH

import os
SOMEONE_RES_PATH = os.path.join(PLUGINS_PATH,'someone_say','resources')

###自定义图
someonesay = on_startswith("有人说", priority=3,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    if len(str(event.message))>10:
        await someonesay.finish()
    await bot.send(event=event,message="茉莉的名人名言系列(需要加上中文冒号哦)~~目前支持\n鲁迅说：\n年号：\n千代：\n宁宁：\nnobeta：\n追杀图：")
    await someonesay.finish()
    

###自定义图
someonesay = on_startswith("鲁迅说：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[4:]
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'luxun.jpg'))
    font_path = os.path.abspath(os.path.join(FONT_PATH, 'msjh.ttf'))
    text_font = ImageFont.truetype(font_path, someone_fig.width // 15)
    
    width = int(someone_fig.width/2)
    text_width = someone_fig.width/5*4
    this_height = int(someone_fig.height*2/3)
    #换行脚本
    last_cut = 0
    for cut in range(len(says)):
        w, h = ImageDraw.Draw(someone_fig).textsize(says[last_cut:cut], font=text_font) 
        if w<text_width:
            continue
        #开始绘图
        ImageDraw.Draw(someone_fig).text(xy = (width, this_height),
                                         text = says[last_cut:cut], align='left',anchor='mb', 
                                         font=text_font,fill=(256, 256, 256))
        this_height += h - 5
        last_cut = cut 
        if this_height >=int(someone_fig.height/10*9):
            await someonesay.finish('太长了，鲁迅说不完...')
            await someonesay.finish() 
    ImageDraw.Draw(someone_fig).text(xy = (width, this_height),
                                    text = says[last_cut:], align='left',anchor='mb', 
                                    font=text_font,fill=(256, 256, 256))         
    #结束换行
    
    ImageDraw.Draw(someone_fig).text(xy=(int(someone_fig.width/10*9), int(someone_fig.height/10*9)),
                                    text='——鲁迅', font=text_font, align='center',anchor='rb',
                                    fill=(256, 256, 256))
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()    
      
###自定义图
someonesay = on_startswith("年号：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[3:]
    if len(says)>2:
        await someonesay.finish('字数超出限制了的说~')    
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'年号.jpg'))
    font_path = os.path.abspath(os.path.join(FONT_PATH, 'msyhbd.ttc'))
    text_font = ImageFont.truetype(font_path, 50)
    
    if len(says) == 2:
        says = says[0]+'\n'+says[1]
        ImageDraw.Draw(someone_fig).multiline_text(xy = (int(160), int(70)),
                                        text = says, align='left', 
                                        font=text_font,fill=(0, 0, 0))     
    else:
        ImageDraw.Draw(someone_fig).multiline_text(xy = (int(160), int(100)),
                                        text = says, align='left', 
                                        font=text_font,fill=(0, 0, 0))     
              
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()    
      
###自定义图
someonesay = on_startswith("宁宁：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[3:]
    if len(says)>=10:
        await someonesay.finish('字数超出限制了的说~')    

    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'宁宁.jpg'))
    font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    text_font = ImageFont.truetype(font_path, 120)
    text_width, text_height = text_font.getsize(says)  
    
    txt=Image.new('L', (800,500))
    d = ImageDraw.Draw(txt)
    d.text(xy=(0,0),text=says, font=text_font, align='left',anchor='lt',fill=255)
    w=txt.rotate(26,  expand=1)
    someone_fig.paste( ImageOps.colorize(w, (0,0,0), (0, 0, 0)), (int(someone_fig.width*30/84-text_width/2), int(text_width/3/2-75)),  w)
    
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()
      
###自定义图
someonesay = on_startswith("千代：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[3:]
    if len(says)>=10:
        await someonesay.finish('字数超出限制了的说~')    
    
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'千代.jpg'))
    font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    text_font = ImageFont.truetype(font_path, 80)
    text_width, text_height = text_font.getsize(says)  
    
    txt=Image.new('L', (500,500))
    d = ImageDraw.Draw(txt)
    d.text(xy=(0,0),text=says, font=text_font, align='left',anchor='lt',fill=255)
    w=txt.rotate(5,  expand=1)
    someone_fig.paste( ImageOps.colorize(w, (0,0,0), (255, 165, 0)), (int(someone_fig.width*0.5-text_width/2), int(someone_fig.height*0.55)),  w)
    
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()
        
someonesay = on_startswith("nobeta：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[7:]
    if len(says)>=10:
        await someonesay.finish('字数超出限制了的说~')        

    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'nobeta.jpg'))
    font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    font = ImageFont.truetype(font_path, someone_fig.width // 10)
    text_width, text_height = font.getsize(says)  
        
    txt=Image.new('L', (500,500))
    d = ImageDraw.Draw(txt)
    d.text(xy=(0,0),text=says, font=font, align='left',anchor='lt',fill=255)
    w=txt.rotate(13,  expand=1)
    someone_fig.paste( ImageOps.colorize(w, (0,0,0), (238, 130, 238)), (int(someone_fig.width*0.5-text_width/2),int(someone_fig.height*0.32)),  w)
    
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()   
        
        
###自定义图
someonesay = on_startswith("追杀图：", priority=5,block=True)
@someonesay.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if not isallow(event,2):
        await someonesay.finish()
    says = str(event.message)[4:]
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    someone_fig = Image.open(os.path.join(SOMEONE_RES_PATH,'追杀.jpg'))
    msjh_font_path = os.path.abspath(os.path.join(FONT_PATH, 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, someone_fig.width // 15)
    text_width, text_height = msjh_text_font.getsize(says)  
    if text_width>=someone_fig.width/3:
        await someonesay.finish('字数超出限制了的说~')
    ImageDraw.Draw(someone_fig).text(xy=(int(someone_fig.width/4), int(someone_fig.height/15*14)),
                                    text=says, font=msjh_text_font, align='center',anchor='mm',
                                    fill=(0, 0, 0))
    someone_fig.save(os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg'), 'JPEG')
    await bot.send(event=event,message=MessageSegment.image(file = "file:///"+os.path.join(SOMEONE_RES_PATH,'ls_fig.jpg')))
    await someonesay.finish()   
