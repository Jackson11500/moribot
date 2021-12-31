import pandas as pd
#columns=['registertime','exp','level','signin','signinexp','signindate','contin_signin','catgirl_to','catgirl_from','cu','pd','ti','th']
main_folder='D://QQ//Bot//nonebot//moribot//src//plugins//user//'
RESOURCES_PATH = 'D://QQ//Bot//nonebot//moribot//resources//'

def register(QQ):
    df_us=pd.read_csv(main_folder+'userdata.csv', index_col=0)
    if QQ in df_us.index:
        return 0
    else:
        import time
        df_us = df_us.append(pd.Series(data={'registertime':round(time.time())},name = QQ)).fillna(0)
        df_us.to_csv(main_folder+'userdata.csv')
        return df_us.shape[0]

def backup():
    import time
    from shutil import copyfile
    localtime = time.localtime(time.time())
    copyfile(main_folder+'userdata.csv', main_folder+f'backup/{localtime.tm_mon}_{localtime.tm_mday}__{localtime.tm_hour}userdata.csv')
    return '文件已备份'

from nonebot.adapters.cqhttp.bot import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from typing import Union
from nonebot.adapters.cqhttp.message import Message, MessageSegment

def req_exp(level):
    return int(3*level*(level+1)/2)

def get_level_color(level: int) -> tuple[int, int, int]:
    '''
    生成图片
    '''
    level_color: dict[int, tuple[int, int, int]] = {
        0: (136, 136, 136),
        1: (102, 102, 102),
        2: (153, 204, 153),
        3: (221, 204, 136),
        4: (255, 204, 51),
        5: (255, 204, 204),
        6: (247, 119, 127),
        7: (102, 204, 255),
        8: (175, 136, 250),
    }
    return level_color.get(level, (136, 136, 136))

def return_level_icon_path(level:int): 
    '''
    返回等级图标所在的文件夹，但这一文件不一定存在
    '''
    unittype = ['','alpha','beta','gamma',
                'dagger','nova','crawler','flare','mono','risso','retusa',
                'mace','pulsar','atrax','horizon','poly','minke','oxynoe',
                'fortress','quasar','spiroct','zenith','mega','bryde','cyerce',
                'scepter','vela','arkyid','antumbra','quad','sei','aegires',
                'reign','corvus','toxopid','eclipse','oct','omura','navanax',
                ]
    return 'D://QQ//Bot//nonebot//moribot//resources//img//mdt//unit//unit-'+unittype[int(level)]+'-full.png'

async def user_sign_in(bot: Bot, event: GroupMessageEvent, state: T_State) -> Union[Message, MessageSegment, str]:
    '''
    处理签到并发送签到图片
    '''
    import pandas as pd
    QQ = event.user_id
    
    msg_box = ""
    df_us=pd.read_csv(main_folder+'userdata.csv', index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    import datetime
    import random
    today = datetime.date.today().timetuple().tm_yday
    
    if QQ not in df_us.index:
        return '茉莉这里还没你的档案呢，要先注册才行哦。输入\'注册\'即可注册茉莉档案'+'\n'
    
    sign_success = True
    if today==int(df_us.loc[QQ].signindate):  
        sign_success = False
        bonus = 0
        cu,pd,ti,th = 0,0,0,0
    else:
        ##签到
        #是否连续签到
        if df_us.loc[QQ].signindate == today-1:
            df_us.loc[QQ,'contin_signin'] += 1
        else:
            df_us.loc[QQ,'contin_signin'] = 1
        #设置签到
        df_us.loc[QQ,'signindate'] = today
        #7日签到
        week = df_us.loc[QQ,'contin_signin']/7
        th = 0
        if week == int(week):
            th = week
            df_us.loc[QQ,'exp']+=3*week
            df_us.loc[QQ,'th']+=th
        #计算随机经验
        exp=random.randrange(1,11,1)    
        df_us.loc[QQ,'signinexp'] = exp
        df_us.loc[QQ,'exp']+=exp
        while df_us.loc[QQ].exp>=req_exp(df_us.loc[QQ].level):
            df_us.loc[QQ,'level']+=1
        bonus = (df_us.loc[QQ].level+exp)*0.01

        if exp==10:
            bonus*=2
        if week == int(week):
            bonus*=2
        
        cu = int(random.randrange(1,21,1)*(1+bonus))
        pd = int(random.randrange(1,16,1)*(1+bonus))
        ti = int(random.random()*3*(1+bonus*2))
        df_us.loc[QQ,'cu']+=cu
        df_us.loc[QQ,'pd']+=pd
        df_us.loc[QQ,'ti']+=ti
        df_us.to_csv(main_folder+'userdata.csv')
    
    
    #完成所有处理，开始画图
    from PIL import Image, ImageDraw, ImageFont
    import os
    nickname = event.sender.card if event.sender.card else event.sender.nickname
    
    width: int = 1024
    height: int = 1024
    
    width_edge = width//20

    # 加载头图
    sign_pic_path = 'D:\\QQ\\Bot\\nonebot\\moribot\\resources\\img\\signin'
    import os
    if f'{QQ}.jpg' in os.listdir(sign_pic_path+'\\user_spec'):
    #if False:
        draw_top_img: Image.Image = Image.open(sign_pic_path+f'\\user_spec\\{QQ}.jpg')
    else:
        filelist = [x for x in os.listdir(sign_pic_path) if os.path.isfile(sign_pic_path+"\\"+ x)]
        random_index = random.randrange(1,len(filelist),1)
        draw_top_img: Image.Image = Image.open(sign_pic_path+"\\"+ filelist[random_index])
    # 调整头图宽度
    top_img_height = int(width * draw_top_img.height / draw_top_img.width)
    draw_top_img = draw_top_img.resize((width, top_img_height))
    if top_img_height>=600:
        draw_top_img = draw_top_img.crop((0,int((top_img_height-600)*1/2),width,top_img_height-int((top_img_height-600)*1/2)))
        top_img_height = 600
    #字体
    bd_font_path = os.path.join(RESOURCES_PATH, 'fonts', 'SourceHanSans_Heavy.otf')
    bd_font = ImageFont.truetype(bd_font_path, width // 20)
    bd_text_font = ImageFont.truetype(bd_font_path, width // 20)    
    
    main_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'SourceHanSans_Regular.otf'))
    text_font = ImageFont.truetype(main_font_path, width // 25)

    level_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'pixel.ttf'))
    level_font = ImageFont.truetype(level_font_path, width // 25)

    monkey_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'HappyMonkey.ttf'))
    monkey_text_font = ImageFont.truetype(monkey_path, width // 20)
    
    mdt_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'tech.ttf'))
    mdt_text_font = ImageFont.truetype(mdt_font_path, width // 25)

    msjh_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, width // 25)

    # 打招呼
    nowtime = datetime.datetime.now()   #现在的时间
    top_text=""
    if 4 <= nowtime.hour < 11:
        top_text = '早上好'
    elif 11 <= nowtime.hour < 14:
        top_text = '中午好'
    elif 14 <= nowtime.hour < 19:
        top_text = '下午好'
    elif 19 <= nowtime.hour < 22:
        top_text = '晚上好'
    else:
        top_text = '晚安'
    
    top_text +=f'，\n@{nickname}'
    top_text_width, top_text_height = bd_font.getsize(top_text)  
    
    #签到说明
    sign_in_text=""
    if sign_success:
        if exp<2:
            sign_in_text+='快跑！！经验+'+str(exp)
        elif exp<4:
            sign_in_text+='好像不妙，经验+'+str(exp)
        elif exp<7:
            sign_in_text+='平平淡淡，经验+'+str(exp)
        elif exp<10:
            sign_in_text+='好运连连，经验+'+str(exp)
        else:
            sign_in_text+='天选之人！经验+'+str(exp) 
        if week == int(week):
            sign_in_text+='(连续签到奖励-额外+'+str(3*week)+')'
        
        sign_in_text+='\n已连续签到'+str(int(df_us.loc[QQ].contin_signin))+'天'
        sign_in_text_width, sign_in_text_height = bd_text_font.getsize(sign_in_text)    
    else:
        sign_in_text+='今日已签到，经验+'+str(int(df_us.loc[QQ,'signinexp']))
        sign_in_text+='\n已连续签到'+str(int(df_us.loc[QQ].contin_signin))+'天'
        sign_in_text_width, sign_in_text_height = bd_text_font.getsize(sign_in_text)   
    
    #经验
    level = int(df_us.loc[QQ].level)
    level_text = f'lv.{level}'    
    exp_text = f'exp={df_us.loc[QQ].exp}' 
    exp_level_text_width, exp_level_text_height = level_font.getsize(level_text)    
    exp_bar = f'{int(df_us.loc[QQ].exp)}/{req_exp(level)}' 
    exp_bar_text_width, exp_bar_text_height = level_font.getsize(exp_bar)   
    #bonus
    bonus_text = f'bonus + {int(bonus*100)}%'
    bonus_text_width, bonus_text_height = mdt_text_font.getsize(exp_bar)   
    
    
    def trans_paste(bg_img,fg_img,box):
        fg_img_trans = Image.new("RGBA",bg_img.size)
        fg_img_trans.paste(fg_img,box,mask=fg_img)
        new_img = Image.alpha_composite(bg_img,fg_img_trans)
        return new_img
    
    def add_trans_paste(background,path, size , box):
        draw_level_img: Image.Image = Image.open(path)
        draw_level_img = draw_level_img.resize((int(draw_level_img.width * size/draw_level_img.height), int(size)))
        return trans_paste(background,draw_level_img,box=box)
    
    background = Image.new(
    mode="RGBA",
    size=(width, int(height)),
    color=(255, 255, 255))
    
    background.paste(draw_top_img,box=(0, 0))
    
    this_height = top_img_height 
    #分隔条
    seperator = 5
    for sepline in range(1,seperator):
        seperator_height = (height - top_img_height- width_edge)/(2*seperator+1)
        ImageDraw.Draw(background).line(xy=[(width/2, top_img_height+seperator_height*(sepline*2+1)),(width/2,top_img_height+seperator_height*sepline*2)],fill=(255, 192, 203), width=int(width_edge/8))  # 备注条 
    
    ##左边
    ImageDraw.Draw(background).multiline_text(xy=(width_edge, this_height),
                                    text=top_text, font=bd_font, align='left',
                                    fill=(0, 0, 0))  # 打招呼

    this_height += top_text_height + height*0.08
    ImageDraw.Draw(background).multiline_text(xy=(width_edge, this_height),
                                                text=sign_in_text, font=text_font, align='left',
                                                fill=(128, 128, 128))  # 签到数据
    
    this_height += sign_in_text_height + height*0.06
    ImageDraw.Draw(background).text(xy=(width_edge, this_height),
                                        text=level_text, font=level_font, align='left',anchor='lt',
                                        fill=(128, 128, 128))  # 等级

    this_height += exp_level_text_height
    # 等级图标
    background = add_trans_paste(background, path = return_level_icon_path(level),
                            size = width // 25,box = (int(width/2)-width_edge-width // 20, int(this_height-width // 22)))
    
    ##经验条
    ImageDraw.Draw(background).rounded_rectangle(xy=[width_edge, this_height, int(width/2)-width_edge, this_height+int(width_edge*2/3)],
                                fill=(224, 224, 224), width=0)  # 经验条底
    
    bar_width = int(  ( (width/2) - 2*width_edge) * ( (df_us.loc[QQ].exp - req_exp(level-1)) / (level*3) )  )
    
    ImageDraw.Draw(background).rounded_rectangle(xy=[width_edge, this_height, width_edge+bar_width, this_height+int(width_edge*2/3)],
                                fill=get_level_color(level=0), width=0)  # 经验条    
    
    ImageDraw.Draw(background).text(xy=(int(width/4), this_height),
                                        text=exp_bar, font=level_font, align='middle',anchor='mt',
                                        fill=(56, 56, 56))  # 经验
    
    
    ##右边
    if sign_success:
        this_height = top_img_height +height*0.025
        ImageDraw.Draw(background).text(xy=(width/4*3, this_height),
                                            text=bonus_text, font=monkey_text_font, align='center',anchor='mt',
                                            fill=(128, 128, 128))  # bonus
        this_height += bonus_text_height+height*0.1
    else:
        this_height = top_img_height + height*0.15    
    ##铜铅钛钍
    #cu
    background = add_trans_paste(background, path = RESOURCES_PATH+str('img//mdt//items//item-copper.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))
    ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{cu}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(217, 157, 115))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'cu'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(217, 157, 115))  # 材料
    #pd
    this_height += height/15
    background = add_trans_paste(background, path = RESOURCES_PATH+str('img//mdt//items//item-lead.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))    
    ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{pd}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(140, 127, 169))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'pd'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(140, 127, 169))  # 材料
    ###ti
    this_height += height/15
    background = add_trans_paste(background, path = RESOURCES_PATH+str('img//mdt//items//item-titanium.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))   
    ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{ti}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(141, 161, 227))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'ti'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(141, 161, 227))  # 材料
    ###th
    this_height += height/15
    background = add_trans_paste(background, path = RESOURCES_PATH+str('img//mdt//items//item-thorium.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))   
    ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{th}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(249, 163, 199))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'th'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(249, 163, 199))  # 材料


    ###末尾
    ruanmeng_font_path = os.path.abspath(os.path.join(RESOURCES_PATH, 'fonts', 'ruanmeng.ttf'))
    ruanmeng_text_font = ImageFont.truetype(ruanmeng_font_path, width // 25)
    ImageDraw.Draw(background).text(xy=(int(width_edge/2), int(height-width_edge/2)),
                                        text='@小狐狸茉莉', font=ruanmeng_text_font, align='middle',anchor='lb',
                                        fill=(255, 105, 180))  # 材料    
    
    ImageDraw.Draw(background).text(xy=(int(width_edge), int(width_edge)),
                                        text='新用户系统删档测试中...将于2022年正式上线！', font=ruanmeng_text_font, align='left',anchor='lt',
                                        fill=(255, 105, 180))  # 材料        
    
    background = background.convert("RGB")
    saveloc = sign_pic_path+f"\\user\\{QQ}_{today}.jpg"
    background.save(saveloc, 'JPEG')
    
    return saveloc
