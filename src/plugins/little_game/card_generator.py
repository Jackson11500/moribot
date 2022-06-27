import sys
sys.path.append("..") 

from PIL import Image, ImageDraw, ImageFont
import os
from configs.path_config import *
from utils.unitTypes import *
import random

Item_Type = ['cu','pd','ti','th']

def trans_paste(bg_img,fg_img,box):
    fg_img_trans = Image.new("RGBA",bg_img.size)
    fg_img_trans.paste(fg_img,box,mask=fg_img)
    new_img = Image.alpha_composite(bg_img,fg_img_trans)
    return new_img

def add_trans_paste(background,path, size , box):
    draw_level_img: Image.Image = Image.open(path)
    draw_level_img = draw_level_img.resize((int(draw_level_img.width * size/draw_level_img.height), int(size)))
    return trans_paste(background,draw_level_img.convert("RGBA"),box=box)

def image_path(num:int,type:int)->str:
    return os.path.join(IMAGE_PATH,'card_deck',f'{int(num)}-{int(type)}.jpg')

def gen_card(number:int,type:int,unittype:str,savepath:str): 
    width = 3000
    height = 4000
    
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
            savepath = image_path(cardnum,cardtype)
            if os.path.exists(savepath):
               continue
            unittype = ''
            if cardnum<10:
                unittype = UNIT_PRO[cardnum][cardtype]
            elif cardtype + (cardnum-10) * 4<10:
                unittype = UNIT_PRO[cardtype + (cardnum-10) * 4][4]
            elif cardtype == 2:
                unittype = 'gamma'
            else:
                unittype = 'emanate'
            gen_card(cardnum + 1,cardtype,unittype,savepath)
            
def gen_math24_game(game_index: int) -> bool:
    '''
    生成math24对应的图片
    '''
    import pandas as pd
    
    width = 4000
    height = 3000
    
    game_deck = pd.read_csv(os.path.join(PLUGINS_PATH,'little_game','math24.csv')).to_numpy()
    
    if game_index == -1:
        
        game_index = random.randint(1,game_deck.shape[0])

    card = np.zeros((4,2))
    card[:,0] = game_deck[game_index,1:5]
    
    #* 设定随机card_type,主要是需要避免重复卡
    cardlist = np.zeros((4))
    card_index = 0
    while card_index<card.shape[0]:
        cardlist[card_index] = -1
        index_type = random.randint(0,3)
        if (card[card_index,0] - 1) * 4 +index_type in cardlist:
            continue
        else:
            cardlist[card_index] = (card[card_index,0] - 1) * 4 +index_type
            card[card_index,1] = index_type
            card_index+=1
    del card_index
    #*打乱
    np.random.shuffle(card)
    
    #* 开始画图
    width = 1667
    height = 1000
    
    background = Image.open(os.path.join(IMAGE_PATH,'card_deck','utils',f'math24_{random.randint(1,5)}.jpg'))
    background = background.resize(size = (width,height))
    background = background.convert("RGBA")
    
    img_height = height * 1/3
    img_width = width * 0.15
    int_width = width * 0.08
    for card_index in range(card.shape[0]):
        background = add_trans_paste(background, path = image_path(card[card_index,0] - 1,card[card_index,1]),
                        size = img_height, box = (int(int_width + (int_width + img_width) * card_index),int(width * 0.21)))
        
    #字体
    bd_font_path = os.path.join(FONT_PATH, 'SourceHanSans_Heavy.otf')
    bd_font = ImageFont.truetype(bd_font_path, int(width * 0.025))
        
    ImageDraw.Draw(background).text(xy=(int(width * 0.5), int(width * 0.457)),
                                text=str(game_index), font=bd_font, align='center',anchor='mm',
                                fill=(0, 0, 0))  #编号
    
    ImageDraw.Draw(background).text(xy=(int(width * 0.5), int(width * 0.486)),
                            text=str(int(game_deck[game_index,6] * 10000)/100), font=bd_font, align='center',anchor='mm',
                            fill=(0, 0, 0))  #答题率
    
    ImageDraw.Draw(background).text(xy=(int(width * 0.512), int(width * 0.515)),
                        text=str(game_deck[game_index,5]), font=bd_font, align='center',anchor='mm',
                        fill=(0, 0, 0))  #时间
    
    ImageDraw.Draw(background).text(xy=(int(width * 0.65), int(width * 0.515)),
                    text=str(game_deck[game_index,8]), font=bd_font, align='center',anchor='mm',
                    fill=(0, 0, 0))  #时间
    
    background = background.convert("RGB")
    background.save(os.path.join(PLUGINS_PATH,'little_game','math24.jpg'), 'JPEG')
    return True