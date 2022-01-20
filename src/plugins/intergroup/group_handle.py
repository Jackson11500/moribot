from nonebot.adapters.cqhttp.bot import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from typing import Union
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from configs.path_config import FONT_PATH,PLUGINS_PATH
import os
THIS_PATH = os.path.join(PLUGINS_PATH,'intergroup')

async def draw_group_status(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    查询并绘制群组状态
    '''
    import os
    from PIL import Image, ImageDraw, ImageFont
    
    
    import pandas as pd
    df=pd.read_csv(os.path.join(PLUGINS_PATH,'group_status.csv'), index_col=0)
    
    
    width = 2000
    height = 1200
    width_edge = width//30
    
    background = Image.new(
    mode="RGBA",
    size=(width, height),
    color=(255, 255, 255))
    
    msjh_font_path = os.path.join(FONT_PATH, 'msjh.ttf')
    msjh_font = ImageFont.truetype(msjh_font_path, width//50)
    msjh_s_font = ImageFont.truetype(msjh_font_path, width//80)
    msjh_ss_font = ImageFont.truetype(msjh_font_path, width//120)
    
    ruanmeng_font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    ruanmeng_s_text_font = ImageFont.truetype(ruanmeng_font_path, width//40)
    ruanmeng_text_font = ImageFont.truetype(ruanmeng_font_path, width//20)
    
    ssmd_font_path = os.path.abspath(os.path.join(FONT_PATH, 'shangshoumengdong.ttf'))
    ssmd_text_font = ImageFont.truetype(ssmd_font_path, width//40)
    
    ##说明及水印
    ImageDraw.Draw(background).text(xy=(width/2, width_edge),
                                    text='>-- 茉莉的群组状态库 --<', font=ruanmeng_text_font, align='left',anchor='mt',
                                    fill=(100, 149, 237))  # 签到数据
    
    ImageDraw.Draw(background).text(xy=(int(width_edge/2), int(height-width_edge/2)),
                                    text='@小狐狸茉莉', font=ruanmeng_s_text_font, align='middle',anchor='lb',
                                    fill=(255, 105, 180))  # 水印   

    ImageDraw.Draw(background).text(xy=(width-int(width_edge/2), int(height-width_edge/2-width//40-20)),
                                    text='共加入11个群，其中6个群隐藏。若要隐藏本群请@lc处理', font=ssmd_text_font, align='middle',anchor='rb',
                                    fill=(150, 150, 150))  #   

    ImageDraw.Draw(background).text(xy=(width-int(width_edge/2), int(height-width_edge/2)),
                                    text='管理权限--更改状态/说明请输入[群组状态设置：状态名：新状态]', font=ssmd_text_font, align='middle',anchor='rb',
                                    fill=(0, 0, 0))  #   
    
    ##表格
    hei_int = height//10    #两组间的间隔
    
    this_width = width_edge + 50
    this_height = 250
    
    #绘制群昵称
    ImageDraw.Draw(background).text(xy=(this_width, this_height-50),
                                text='-->状态名', font=msjh_ss_font, align='m',anchor='mb',
                                fill=(255, 0, 0))
    ImageDraw.Draw(background).text(xy=(this_width, this_height),
                                text='群号', font=msjh_font, align='m',anchor='mm',
                                fill=(102, 51, 153))
    for group_index in range(len(df.index[1:])):
        if df.loc[df.index[group_index+1],'hidden'] == '1':
            continue
        this_height += hei_int
        ImageDraw.Draw(background).text(xy=(this_width, this_height),
                                    text=df.index[group_index+1], font=msjh_font, align='m',anchor='mm',
                                    fill=(102, 51, 153))
        
    this_height = 250
    #群名及说明（画在一起）
    font_width,font_height = msjh_font.getsize(df.loc['des','group_name'])
    this_width += 300
    ImageDraw.Draw(background).text(xy=(this_width, this_height-50),
                                text='group_name|intro', font=msjh_ss_font, align='m',anchor='mb',
                                fill=(255, 0, 0))
    ImageDraw.Draw(background).text(xy=(this_width, this_height-int(font_height/2)),
                                text=df.loc['des','group_name'], font=msjh_s_font, align='m',anchor='mm',
                                fill=(255, 99, 71))
    ImageDraw.Draw(background).text(xy=(this_width, this_height+int(font_height/2)),
                                text=df.loc['des','intro'], font=msjh_s_font, align='m',anchor='mm',
                                fill=(255, 140, 0))
    for group_index in range(len(df.index[1:])):
        if df.loc[df.index[group_index+1],'hidden'] == '1':
            continue
        this_height += hei_int
        ImageDraw.Draw(background).text(xy=(this_width, this_height-int(font_height/2)),
                                    text=df.loc[df.index[group_index+1],'group_name'], font=msjh_s_font, align='m',anchor='mm',
                                    fill=(255, 99, 71))
        ImageDraw.Draw(background).text(xy=(this_width, this_height+int(font_height/2)),
                                    text=df.loc[df.index[group_index+1],'intro'], font=msjh_s_font, align='m',anchor='mm',
                                    fill=(255, 140, 0))
    
    this_width = this_width + 100
    
    for type in df.columns[3:]:
        this_height = 250
        
        font_width,font_height = msjh_font.getsize(df.loc['des',type])
        this_width += 200
        ImageDraw.Draw(background).text(xy=(this_width, this_height-50),
                                    text=type, font=msjh_ss_font, align='m',anchor='mb',
                                    fill=(255, 0, 0))
        ImageDraw.Draw(background).text(xy=(this_width, this_height),
                                    text=df.loc['des',type], font=msjh_s_font, align='m',anchor='mm',
                                    fill=(0, 0, 0))
        for group_index in range(len(df.index[1:])):
            if df.loc[df.index[group_index+1],'hidden'] == '1':
                continue
            this_height += hei_int
            if df.loc[df.index[group_index+1],type] == '1':
                ImageDraw.Draw(background).text(xy=(this_width, this_height),
                                            text='开启', font=msjh_s_font, align='m',anchor='mm',
                                            fill=(34, 139, 34))
            else:
                ImageDraw.Draw(background).text(xy=(this_width, this_height),
                                            text='关闭', font=msjh_s_font, align='m',anchor='mm',
                                            fill=(255, 0, 0))                
        
    background = background.convert("RGB")
    save_path = os.path.join(THIS_PATH,'ls_image','ls_group_status.jpg')
    background.save(save_path, 'JPEG')
    return save_path
    