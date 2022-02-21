import pandas as pd
columns=['registertime','exp','level','signin','signinexp','signindate','contin_signin','cu','pd','ti','th','catgirl_to','catgirl_from']

from configs.path_config import PLUGINS_PATH, USER_PATH,IMAGE_PATH,FONT_PATH,MAIN_PATH
import os
THIS_PATH = os.path.join(PLUGINS_PATH,'user')

def register(QQ):
    import os
    user_path = os.path.join(USER_PATH, str(QQ))
    if os.path.exists(user_path):
        return 0 
    else:
        import time
        os.mkdir(user_path)
        df = pd.DataFrame(columns=columns).append(pd.Series(data={'registertime':round(time.time())},name = QQ)).fillna(0)
        df.to_csv(os.path.join(USER_PATH, str(QQ),'data.csv'))
        return len(os.listdir(USER_PATH))

def backup():
    import time,os,shutil
    localtime = time.localtime(time.time())
    shutil.copytree(USER_PATH, os.path.join(MAIN_PATH, 'data','databackup',f'{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}'))
    return '文件已备份'

from nonebot.adapters.cqhttp.bot import Bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from typing import Union
from nonebot.adapters.cqhttp.message import Message, MessageSegment

def req_exp(level):
    return int(3*level*(level+1)/2)

def get_level_color(level: int):
    '''
    生成图片
    '''
    level_color: dict[int, tuple[int, int, int]] = {
        0: (192, 192, 192),
        1: (102, 102, 102),
        2: (100, 149, 237),
        3: (20, 255, 255),
        4: (20, 255, 127),
        5: (255, 215, 20),
        6: (255, 145, 20),
        7: (255, 127, 80),
        8: (255, 20, 255),
        9: (255, 0, 0),
    }
    return level_color.get(level, (136, 136, 136))

def return_level_icon_path(level:int): 
    '''
    返回等级图标所在的文件夹，但这一文件不一定存在
    '''
    unittype = ['','alpha','beta','gamma',
                'dagger','crawler','nova','flare','mono','risso','retusa',
                'mace','atrax','pulsar','horizon','poly','minke','oxynoe',
                'fortress','spiroct','quasar','zenith','mega','bryde','cyerce',
                'scepter','arkyid','vela','antumbra','quad','sei','aegires',
                'reign','toxopid','corvus','eclipse','oct','omura','navanax',
                ]
    return 'D://QQ//Bot//nonebot//moribot//resources//img//mdt//unit//unit-'+unittype[int(level)]+'-full.png'

async def user_sign_in(bot: Bot, event: GroupMessageEvent, state: T_State) -> Union[Message, MessageSegment, str]:
    '''
    处理签到并发送签到图片3
    '''
    QQ = event.user_id
    import pandas
    import os
    if not os.path.exists(os.path.join(USER_PATH, str(QQ))):
        return '茉莉这里还没你的档案呢，要先注册才行哦。输入\'注册\'即可注册茉莉档案'+'\n'
    
    df_us=pandas.read_csv(os.path.join(USER_PATH, str(QQ),'data.csv'), index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    
    import datetime
    import random
    today = datetime.date.today().timetuple().tm_yday
    
    sign_success = True #是否签到成功
    cu,pd,ti,th = 0,0,0,0
    exp = 0
    bonus = 0
    
    #计算周六日加成
    week = datetime.datetime.now().weekday()
    if week == 4:
        bonus += 5 * 0.01
    elif week > 4:
        bonus += 10 * 0.01   
    else:
        bonus += int(random.random()*5) * 0.01
    
    #计算成就加成
    ACH_PATH = os.path.join(USER_PATH, str(QQ),'achievement.csv')
    if os.path.exists(ACH_PATH):
        df_ach=pandas.read_csv(ACH_PATH, index_col=0)
        for index, row in df_ach.iterrows():
            exp += int(row['daily_exp'])
            cu += int(row['daily_cu'])
            pd += int(row['daily_pd'])
            ti += int(row['daily_ti'])
            th += int(row['daily_th'])
            bonus += int(row['bonus'])*0.01
        del df_ach
        
    #主加成程序
    if today==int(df_us.loc[QQ].signindate):  #! 计算个人信息
        exp +=int(df_us.loc[QQ,'signinexp'])
        
        sign_success = False
        bonus += (df_us.loc[QQ].level+df_us.loc[QQ].signinexp) * 0.01

        if df_us.loc[QQ].signinexp==10:
            bonus*=2
        if df_us.loc[QQ,'contin_signin'] % 5 == 0:
            bonus*=2
        if today == 32:
            bonus += 0.1*max(df_us.loc[QQ,'contin_signin'],10)
            exp = max(exp,2)+25
            cu += 25
            pd += 25
            ti += 10
            th += 3
        
        while df_us.loc[QQ].exp>=req_exp(df_us.loc[QQ].level):
            df_us.loc[QQ,'level']+=1
        
    else:
        ##! 签到
        #是否连续签到
        if df_us.loc[QQ].signindate == today-1:
            df_us.loc[QQ,'contin_signin'] += 1
        elif df_us.loc[QQ,'contin_signin']>=5:
            df_us.loc[QQ,'contin_signin'] -= 4
        else:
            df_us.loc[QQ,'contin_signin'] = 1
        #设置签到
        df_us.loc[QQ,'signindate'] = today
        #7日签到
        week = df_us.loc[QQ,'contin_signin']/7
        if week == int(week):
            th += 1
            df_us.loc[QQ,'exp']+=3*week
            
        #计算随机经验的加成
        random_exp=random.randrange(1,11,1)    
        if random_exp==10 and random.random()>=0.9:#* 超级幸运
            random_exp*=2
        exp+=random_exp

        bonus += (df_us.loc[QQ].level+exp)*0.01

        if random_exp>=10:
            if random_exp==20:
                bonus*=2.5
            bonus*=2
        
        if df_us.loc[QQ,'contin_signin']%5 == 0:
            bonus*=2
        
        if today == 32:
            bonus += 0.1*max(df_us.loc[QQ,'contin_signin'],10)
            exp = max(exp,2)+25
            cu += 25
            pd += 25
            ti += 10
            th += 3
        
        cu += int(random.random()*20*(1+bonus))
        pd += int(random.random()*15*(1+bonus))
        ti += int(random.random()*3*(1+bonus))
        th += int(random.random()*0.6*(1+bonus))
        
        df_us.loc[QQ,'signinexp'] = random_exp
        df_us.loc[QQ,'exp']+=exp
        df_us.loc[QQ,'cu']+=cu
        df_us.loc[QQ,'pd']+=pd
        df_us.loc[QQ,'ti']+=ti
        df_us.loc[QQ,'th']+=th
        
        while df_us.loc[QQ].exp>=req_exp(df_us.loc[QQ].level):
            df_us.loc[QQ,'level']+=1
        #保存
        df_us.to_csv(os.path.join(USER_PATH, str(QQ),'data.csv'))
    
    #完成所有处理，开始画图
    from PIL import Image, ImageDraw, ImageFont
    import os
    nickname = event.sender.card if event.sender.card else event.sender.nickname
    
    width: int = 1024
    height: int = 1024
    
    width_edge = width//20

    # 加载头图
    sign_pic_path = os.path.join(IMAGE_PATH,'signin')
    background_lock=0   #锁定背景？，1为锁定
    if os.path.exists(os.path.join(USER_PATH, str(QQ),'background')):
        filelist = [x for x in os.listdir(os.path.join(USER_PATH, str(QQ),'background')) if os.path.isfile(os.path.join(USER_PATH, str(QQ),'background',x))]
        random_index = random.randrange(1,len(filelist),1)
        draw_top_img: Image.Image = Image.open(os.path.join(USER_PATH, str(QQ),'background',filelist[random_index]))
        background_lock=2
    elif os.path.exists(os.path.join(USER_PATH, str(QQ),'background.jpg')):
        draw_top_img: Image.Image = Image.open(os.path.join(USER_PATH, str(QQ),'background.jpg'))
        background_lock=1
    else:
        filelist = [x for x in os.listdir(sign_pic_path) if os.path.isfile(os.path.join(sign_pic_path,x))]
        random_index = random.randrange(1,len(filelist),1)
        draw_top_img: Image.Image = Image.open(os.path.join(sign_pic_path,filelist[random_index]))
        
    # 调整头图宽度
    top_img_height = int(width * draw_top_img.height / draw_top_img.width)
    draw_top_img = draw_top_img.resize((width, top_img_height))
    if top_img_height>=600:
        draw_top_img = draw_top_img.crop((0,int((top_img_height-600)*1/2),width,top_img_height-int((top_img_height-600)*1/2)))
        top_img_height = 600
    #字体
    bd_font_path = os.path.join(FONT_PATH, 'SourceHanSans_Heavy.otf')
    bd_font = ImageFont.truetype(bd_font_path, width // 20)
    bd_text_font = ImageFont.truetype(bd_font_path, width // 20)    
    
    main_font_path = os.path.abspath(os.path.join(FONT_PATH, 'SourceHanSans_Regular.otf'))
    text_font = ImageFont.truetype(main_font_path, width // 25)

    level_font_path = os.path.abspath(os.path.join(FONT_PATH, 'pixel.ttf'))
    level_font = ImageFont.truetype(level_font_path, width // 25)

    monkey_path = os.path.abspath(os.path.join(FONT_PATH, 'HappyMonkey.ttf'))
    monkey_text_font = ImageFont.truetype(monkey_path, width // 20)
    
    mdt_font_path = os.path.abspath(os.path.join(FONT_PATH, 'tech.ttf'))
    mdt_text_font = ImageFont.truetype(mdt_font_path, width // 25)

    msjh_font_path = os.path.abspath(os.path.join(FONT_PATH, 'msjh.ttf'))
    msjh_text_font = ImageFont.truetype(msjh_font_path, width // 25)
    
    ruanmeng_font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    ruanmeng_text_font = ImageFont.truetype(ruanmeng_font_path, width // 25)
    ruanmeng_ss_text_font = ImageFont.truetype(ruanmeng_font_path, width // 40)

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
    
    if today == 32:
        sign_in_text+='新年快乐！！经验+'+str(exp)
        sign_in_text+='\n已连续签到'+str(int(df_us.loc[QQ].contin_signin))+'天'
        sign_in_text_width, sign_in_text_height = bd_text_font.getsize(sign_in_text)
    elif sign_success:
        if random_exp<2:
            sign_in_text+='快跑！！经验+'+str(exp)
        elif random_exp<4:
            sign_in_text+='好像不妙，经验+'+str(exp)
        elif random_exp<7:
            sign_in_text+='平平淡淡，经验+'+str(exp)
        elif random_exp<10:
            sign_in_text+='好运连连，经验+'+str(exp)
        elif random_exp==10:
            sign_in_text+='天选之人！经验+'+str(exp) 
        else:
            sign_in_text+='万里挑一！！经验+'+str(exp) 
        #if week == int(week):
        #    sign_in_text+='(连续签到奖励-额外+'+str(3*week)+')'
        
        sign_in_text+='\n已连续签到'+str(int(df_us.loc[QQ].contin_signin))+'天'
        sign_in_text_width, sign_in_text_height = bd_text_font.getsize(sign_in_text)    
    else:
        sign_in_text+='今日已签到，经验+'+str(exp)
        sign_in_text+='\n已连续签到'+str(int(df_us.loc[QQ].contin_signin))+'天'
        sign_in_text_width, sign_in_text_height = bd_text_font.getsize(sign_in_text)   
    
    #经验
    level = int(df_us.loc[QQ].level)
    level_text = f'lv.{level}'    
    exp_text = f'exp={df_us.loc[QQ].exp}' 
    exp_level_text_width, exp_level_text_height = level_font.getsize(level_text)    
    exp_bar = f'{int(df_us.loc[QQ].exp)}/{req_exp(level)}'  
    #bonus
    bonus_text = f'bonus + {int(bonus*100)} %'
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
    if background_lock == 1:
        this_height = top_img_height +height*0.02
        ImageDraw.Draw(background).text(xy=(int(width-width_edge/2), int(this_height)),
                                            text='[已锁定背景]', font=ruanmeng_ss_text_font, align='middle',anchor='rt',
                                            fill=(153, 51, 255))  # 材料
    elif background_lock == 2:
        this_height = top_img_height +height*0.02
        ImageDraw.Draw(background).text(xy=(int(width-width_edge/2), int(this_height)),
                                            text='[已锁定背景池]', font=ruanmeng_ss_text_font, align='middle',anchor='rt',
                                            fill=(153, 51, 255))  # 材料
    this_height = top_img_height +height*0.05
    ImageDraw.Draw(background).text(xy=(width/4*3, this_height),
                                        text=bonus_text, font=monkey_text_font, align='center',anchor='mt',
                                        fill=get_level_color(level=min(9,int(bonus*10))))  # bonus
    this_height += bonus_text_height+height*0.075
    
    ##铜铅钛钍
    #cu
    background = add_trans_paste(background, path = os.path.join(IMAGE_PATH, 'mdt','items','item-copper.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))
    if sign_success:
        ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{cu}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(217, 157, 115))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'cu'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(217, 157, 115))  # 材料
    #pd
    this_height += height/15
    background = add_trans_paste(background, path = os.path.join(IMAGE_PATH, 'mdt','items','item-lead.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))    
    if sign_success:
        ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{pd}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(140, 127, 169))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'pd'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(140, 127, 169))  # 材料
    ###ti
    this_height += height/15
    background = add_trans_paste(background, path = os.path.join(IMAGE_PATH, 'mdt','items','item-titanium.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))   
    if sign_success:
        ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                        text=f'+{ti}', font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(141, 161, 227))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'ti'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(141, 161, 227))  # 材料
    ###th
    this_height += height/15
    background = add_trans_paste(background, path = os.path.join(IMAGE_PATH, 'mdt','items','item-thorium.png'),
                            size = width // 22,box = (int(width/2)+width_edge, int(this_height)))   
    if sign_success:
        ImageDraw.Draw(background).text(xy=(int(width/4*3), int(this_height)),
                                            text=f'+{th}', font=msjh_text_font, align='middle',anchor='mt',
                                            fill=(249, 163, 199))  # 材料
    ImageDraw.Draw(background).text(xy=(int(width-2*width_edge), int(this_height)),
                                        text=str(int(df_us.loc[QQ,'th'])), font=msjh_text_font, align='middle',anchor='mt',
                                        fill=(249, 163, 199))  # 材料

    ###末尾
    ImageDraw.Draw(background).text(xy=(int(width_edge/2), int(height-width_edge/2)),
                                        text='@小狐狸茉莉', font=ruanmeng_text_font, align='middle',anchor='lb',
                                        fill=(255, 105, 180))  # 材料      
    
    background = background.convert("RGB")
    saveloc = sign_pic_path+f"\\user\\{QQ}_{today}.jpg"
    background.save(saveloc, 'JPEG')
    
    return saveloc

def combine_user_data():
    import os
    combine_ud = pd.read_csv(os.path.join(USER_PATH, '853330464','data.csv'), index_col=0)
    combine_ud['registertime'] = combine_ud['registertime'].apply(str) + '\t'
    for folder in os.listdir(USER_PATH):
        if folder == '853330464':
            continue
        df_us=pd.read_csv(os.path.join(USER_PATH, folder,'data.csv'), index_col=0)
        df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
        combine_ud = combine_ud.append(df_us).fillna(0)
        
    combine_ud.to_csv(os.path.join(MAIN_PATH,'data','alluserdata.csv'))

def ranking_list():
    import os
    df_us = pd.read_csv(os.path.join(MAIN_PATH,'data','alluserdata.csv'), index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    
    df_us_act = df_us[df_us['contin_signin'] >= df_us['contin_signin'].max()*0.8]

    from PIL import Image, ImageDraw, ImageFont
    width = 2000
    height = 2600
    width_edge = width//30
    
    background = Image.new(
    mode="RGBA",
    size=(width, height),
    color=(255, 255, 255))
    
    msjh_font_path = os.path.join(FONT_PATH, 'msjh.ttf')
    msjh_font = ImageFont.truetype(msjh_font_path, 80)
    msjh_l_font = ImageFont.truetype(msjh_font_path, 120)
    msjh_ss_font = ImageFont.truetype(msjh_font_path, width//120)
    
    ruanmeng_font_path = os.path.abspath(os.path.join(FONT_PATH, 'ruanmeng.ttf'))
    ruanmeng_s_text_font = ImageFont.truetype(ruanmeng_font_path, 120)
    ruanmeng_text_font = ImageFont.truetype(ruanmeng_font_path, 120)
    
    ssmd_font_path = os.path.abspath(os.path.join(FONT_PATH, 'shangshoumengdong.ttf'))
    ssmd_text_font = ImageFont.truetype(ssmd_font_path, 120)
    
    
    # 加载头图
    draw_top_img: Image.Image = Image.open(os.path.join(IMAGE_PATH,'signin',"FHD_BG_02.jpg"))
    # 调整头图宽度
    top_img_height = int(width * draw_top_img.height / draw_top_img.width)
    draw_top_img = draw_top_img.resize((width, top_img_height))
    if top_img_height>=1200:
        draw_top_img = draw_top_img.crop((0,int((top_img_height-1200)*1/2),width,top_img_height-int((top_img_height-1200)*1/2)))
        top_img_height = 1200
    background.paste(draw_top_img,box=(0, 0))
    
    
    
    ##说明及水印
    ImageDraw.Draw(background).text(xy=(width/2, width_edge+top_img_height),
                                    text='>-- 茉莉的用户排行榜 --<', font=ruanmeng_text_font, align='left',anchor='mt',
                                    fill=(100, 149, 237))  # 签到数据
    
    ImageDraw.Draw(background).text(xy=(int(width_edge/2), int(height-width_edge/2)),
                                    text='@小狐狸茉莉', font=ruanmeng_text_font, align='middle',anchor='lb',
                                    fill=(255, 105, 180))  # 水印   
    ImageDraw.Draw(background).text(xy=(width - int(width_edge/2), int(height-width_edge/2)),
                                    text=f'总人数：{int(df_us.shape[0])}', font=ssmd_text_font, align='middle',anchor='rb',
                                    fill=(255, 0, 0))  # 总人数   
    
    this_height =250+top_img_height
    interval = 30*4
    
    locx_type = int(width * 1/5)
    locx_median = int(width * 2/5)
    locx_ave = int(width * 3/5)
    locx_max = int(width * 4/5)
    
    def draw_line(y,n_type,median,ave,max):
        ImageDraw.Draw(background).text(xy=(locx_type,y),
                                        text=n_type, font=msjh_font, align='m',anchor='mt',
                                        fill=(255, 102, 51))  # 首行
        ImageDraw.Draw(background).text(xy=(locx_median,y),
                                        text=str(median), font=msjh_font, align='m',anchor='mt',
                                        fill=(115, 0, 230))  # 中位数       
        ImageDraw.Draw(background).text(xy=(locx_ave,y),
                                        text=str(ave), font=msjh_font, align='m',anchor='mt',
                                        fill=(51, 51, 255))  # 平均   
        ImageDraw.Draw(background).text(xy=(locx_max,y),
                                        text=str(max), font=msjh_font, align='m',anchor='mt',
                                        fill=(255, 51, 51))  # 最高

    def draw_line_num(y,n_type,median,ave,max):
        ImageDraw.Draw(background).text(xy=(locx_type,y),
                                        text=n_type, font=msjh_font, align='m',anchor='mt',
                                        fill=(255, 102, 51))  # 首行
        median=round(median,1)
        ave=round(ave,1)
        max=int(max)
        ImageDraw.Draw(background).text(xy=(locx_median,y),
                                        text=str(median), font=msjh_font, align='m',anchor='mt',
                                        fill=(115, 0, 230))  # 中位数       
        ImageDraw.Draw(background).text(xy=(locx_ave,y),
                                        text=str(ave), font=msjh_font, align='m',anchor='mt',
                                        fill=(51, 51, 255))  # 平均   
        ImageDraw.Draw(background).text(xy=(locx_max,y),
                                        text=str(max), font=msjh_font, align='m',anchor='mt',
                                        fill=(255, 51, 51))  # 最高
    
    def draw_line_pic(background,y,item_name,median,ave,max):
        
        def add_trans_paste(background,path, size , box):
            def trans_paste(bg_img,fg_img,box):
                fg_img_trans = Image.new("RGBA",bg_img.size)
                fg_img_trans.paste(fg_img,box,mask=fg_img)
                new_img = Image.alpha_composite(bg_img,fg_img_trans)
                return new_img
            draw_level_img: Image.Image = Image.open(path)
            draw_level_img = draw_level_img.resize((int(draw_level_img.width * size/draw_level_img.height), int(size)))
            return trans_paste(background,draw_level_img,box=box)
        
        background = add_trans_paste(background, path = os.path.join(IMAGE_PATH, 'mdt','items',f'item-{item_name}.png'),
                                size = 80,box = (locx_type-20, y))
        
        median=round(median,1)
        ave=round(ave,1)
        max=int(max)
        ImageDraw.Draw(background).text(xy=(locx_median,y),
                                        text=str(median), font=msjh_font, align='m',anchor='mt',
                                        fill=(115, 0, 230))  # 中位数       
        ImageDraw.Draw(background).text(xy=(locx_ave,y),
                                        text=str(ave), font=msjh_font, align='m',anchor='mt',
                                        fill=(51, 51, 255))  # 平均   
        ImageDraw.Draw(background).text(xy=(locx_max,y),
                                        text=str(max), font=msjh_font, align='m',anchor='mt',
                                        fill=(255, 51, 51))  # 最高
        return background


    draw_line(this_height,'属性|材料','全体平均','活跃平均','最高分！')
    
    this_height = this_height+interval
    draw_line_num(this_height,'经验值',df_us['exp'].mean(),df_us_act['exp'].mean(),df_us['exp'].max())
    
    this_height = this_height+interval
    draw_line_num(this_height,'连续签到',df_us['contin_signin'].mean(),df_us_act['contin_signin'].mean(),df_us['contin_signin'].max())
    
    this_height = this_height+interval
    draw_line_num(this_height,'-等级-',df_us['level'].mean(),df_us_act['level'].mean(),df_us['level'].max())
    
    this_height = this_height+interval+30
    background=draw_line_pic(background,this_height,'copper',df_us['cu'].mean(),df_us_act['cu'].mean(),df_us['cu'].max())

    this_height = this_height+interval
    background=draw_line_pic(background,this_height,'lead',df_us['pd'].mean(),df_us_act['pd'].mean(),df_us['pd'].max())
    
    this_height = this_height+interval
    background=draw_line_pic(background,this_height,'titanium',df_us['ti'].mean(),df_us_act['ti'].mean(),df_us['ti'].max())
    
    this_height = this_height+interval
    background=draw_line_pic(background,this_height,'thorium',df_us['th'].mean(),df_us_act['th'].mean(),df_us['th'].max())
    
    background = background.convert("RGB")
    saveloc = os.path.join(THIS_PATH,'ls_image','ranking_list.jpg')
    background.save(saveloc, 'JPEG')
