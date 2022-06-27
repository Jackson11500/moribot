import sys
sys.path.append("..") 

from PIL import Image, ImageDraw, ImageFont
import os
from configs.path_config import *
from utils.unitTypes import *

Item_Type = ['cu','pd','ti','th']

def trans_paste(bg_img,fg_img,box):
    fg_img_trans = Image.new("RGBA",bg_img.size)
    fg_img_trans.paste(fg_img,box,mask=fg_img)
    new_img = Image.alpha_composite(bg_img,fg_img_trans)
    return new_img

def add_trans_paste(background,path, size , box):
    draw_level_img: Image.Image = Image.open(path)
    draw_level_img = draw_level_img.resize((int(draw_level_img.width * size/draw_level_img.height), int(size)))
    return trans_paste(background,draw_level_img,box=box)

def gen_card(number:int,type:int,unittype:str,savepath:str): 
    width = 750
    height = 1000
    
    mdt_text_font = ImageFont.truetype(os.path.join(FONT_PATH, 'Sounso-Rare-2.ttf'), int(width * 0.2))
    
    background = Image.open(os.path.join(IMAGE_PATH,'card_deck','utils',f'{Item_Type[type]}_background.jpg'))
    background = background.resize(size = (width,height))
    background = background.convert("RGBA")
    
    #左上、右下字体
    if number>10:
        number = ['J','Q','K'][number - 11]
    ImageDraw.Draw(background).text(xy=(int(width * 0.15), int(height * 0.1)),
                                    text=str(number), font=mdt_text_font, align='center',anchor='mm',
                                    fill=(128, 128, 128))  # 等级
    ImageDraw.Draw(background).text(xy=(int(width * 0.85), int(height * 0.9)),
                                text=str(number), font=mdt_text_font, align='center',anchor='mm',
                                fill=(128, 128, 128))  # 等级
    
    img_size = int(width * 0.3)
    background = add_trans_paste(background, path = ui_image_path('unit',unittype),
                        size = img_size,box = (int(width * 0.5 - img_size /2 ),int(height*0.5 - img_size/2)))
    
    background = background.convert("RGB")
    background.save(savepath, 'JPEG')
    
def gen_all_card():
    for cardtype in range(4):
        for cardnum in range(13):
            savepath = os.path.join(IMAGE_PATH,'card_deck',f'{cardnum}-{cardtype}.jpg')
            if os.path.exists(savepath):
               continue
            unittype = ''
            if cardnum<10:
                unittype = UNIT_PRO[cardnum][cardtype]
            elif cardtype + (cardnum-10) * 4<10:
                unittype = UNIT_PRO[cardtype + (cardnum-10) * 4][4]
            elif cardtype == 2:
                unittype = 'alpha'
            else:
                unittype = 'evoke'
            gen_card(cardnum + 1,cardtype,unittype,savepath)