import pandas as pd
ach_col=['acquiretime','ach_name','level','daily_exp','daily_cu','daily_pd','daily_ti','daily_th','bonus']

from configs.path_config import PLUGINS_PATH, USER_PATH,IMAGE_PATH,FONT_PATH,MAIN_PATH
import os
THIS_PATH = os.path.join(PLUGINS_PATH,'user')

achievement_list = {'图片收藏家'}   #level=多少张图,one_cu = level//10,one_pd = level//10, bonus = level//100
from src.plugins.user.databank import achievement
'''
图片收藏家成就：发送高质量图片满100张并成功被茉莉收录进'随机图片系列'即可。
每100张图获得永久1% bonus(吃bonus倍率加成)
每10张图获得1铜1铅
如有遗漏，请私戳茉莉或者@lc补充!
同时欢迎大家向茉莉发送新的图包
''' 
achi_list ={
    853330464:['lc',1500],
    2114592478:['瑶瑶',1500],
    1030767312:['工业2',121],
    3391867495:['小屑猫',114],
    2593890337:['小恶魔',200],
    1456616666:['carrot',655],
    570342546:['大猫',108],
    2361832829:['白猫',500],
    2035768867:['pama',138],
    3489547115:['天幻',50]
}


def add_achievement(QQ,ach_name,level, one_exp=0 ,one_cu = 0,one_pd = 0,one_ti = 0,one_th = 0):
    '''
    增加一个成就，返回说明
    '''
    import time
    if not os.path.exists(os.path.join(USER_PATH, str(QQ))):
        return 0

    achi = {'acquiretime':round(time.time()),
            'ach_name':ach_name,
            'level':level,
            'daily_exp':int(achievement[ach_name]['daily_exp']*level),
            'daily_cu':int(achievement[ach_name]['daily_exp']*level),
            'daily_pd':int(achievement[ach_name]['daily_pd']*level),
            'daily_ti':int(achievement[ach_name]['daily_ti']*level),
            'daily_th':int(achievement[ach_name]['daily_th']*level),
            'bonus':int(achievement[ach_name]['bonus']*level)
            }
    
    ACH_PATH = os.path.join(USER_PATH, str(QQ),'achievement.csv')
    if not os.path.exists(ACH_PATH):
        df_ach = pd.DataFrame(columns=ach_col).append(pd.Series(data=achi,name = QQ)).fillna(0)
        df_ach.to_csv(ACH_PATH)
    else:
        df_ach=pd.read_csv(ACH_PATH, index_col=0)
        df_ach['acquiretime'] = df_ach['acquiretime'].apply(str) + '\t'
        if not ach_name in df_ach.ach_name.tolist():
            df_ach.append(pd.Series(data=achi,name = QQ)).fillna(0)
            df_ach.to_csv(ACH_PATH)
        else:
            row = df_ach.index.tolist()[df_ach.ach_name.tolist().index(ach_name)]
            df_ach.loc[row,'level'] += achi['level']
            for col in df_ach.columns.tolist()[3:]:
                df_ach.loc[row,col] = int(df_ach.loc[row,'level'] * achievement[ach_name][col])
            df_ach.to_csv(ACH_PATH)
    
    df_us=pd.read_csv(os.path.join(USER_PATH, str(QQ),'data.csv'), index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    df_us.loc[QQ,'exp']+=one_exp
    df_us.loc[QQ,'cu']+=one_cu
    df_us.loc[QQ,'pd']+=one_pd
    df_us.loc[QQ,'ti']+=one_ti
    df_us.loc[QQ,'th']+=one_th
    #保存
    df_us.to_csv(os.path.join(USER_PATH, str(QQ),'data.csv'))
    return 1
    
