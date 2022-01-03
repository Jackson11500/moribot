from configs.path_config import USER_PATH
from src.plugins.user.databank import service_list

def modify_res(QQ ,level = 0, cu = 0,pd = 0, ti = 0,th = 0):
    '''
    检验并处理消耗资源\n
    如果没有账户，返回 0\n
    如果缺等级，返回 0\n
    如果缺铜铅钛钍，分别返回 1,2,3,4\n
    如果成功处理，返回 99
    '''
    import os
    import pandas
    
    if not os.path.exists(os.path.join(USER_PATH, str(QQ))):
        return 0
    
    df_us=pandas.read_csv(os.path.join(USER_PATH, str(QQ),'data.csv'), index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    
    if level > int(df_us.level):
        return 0
    
    #先检验全部资源都够
    if cu < 0 and int(df_us.cu) + cu <0:
        return 1
    if pd < 0 and int(df_us.pd) + pd <0:
        return 2
    if ti < 0 and int(df_us.ti) + ti <0:
        return 3
    if th < 0 and int(df_us.th) + th <0:
        return 4
    
    #满足，开始处理数据
    df_us.cu+=cu
    df_us.pd+=pd
    df_us.ti+=ti
    df_us.th+=th
    
    #保存
    df_us.to_csv(os.path.join(USER_PATH, str(QQ),'data.csv'))
    return 99

def check_service(QQ ,service):
    '''
    检验并支付服务开销

    如果服务项不存在，返回 -1\n
    如果缺少账号或等级，返回 0 \n
    如果缺铜铅钛钍，分别返回 1,2,3,4\n
    如果成功处理，返回 99
    '''
    import os
    import pandas
    
    if service not in service_list:
        return -1
    
    if service_list[service]['level'] <0:   #不需要等级
        return 99
    
    if not os.path.exists(os.path.join(USER_PATH, str(QQ))):
        return 0
        
    df_us=pandas.read_csv(os.path.join(USER_PATH, str(QQ),'data.csv'), index_col=0)
    df_us['registertime'] = df_us['registertime'].apply(str) + '\t'
    
    if service_list[service]['level'] > int(df_us.level):
        return 0
    
    #先检验全部资源都够
    if int(df_us.cu) < service_list[service]['cu']:
        return 1
    if int(df_us.pd)  < service_list[service]['pd']:
        return 2
    if int(df_us.ti)  < service_list[service]['ti']:
        return 3
    if int(df_us.th) < service_list[service]['th']:
        return 4
    
    #满足，开始处理数据
    df_us.cu-=service_list[service]['cu']
    df_us.pd-=service_list[service]['pd']
    df_us.ti-=service_list[service]['ti']
    df_us.th-=service_list[service]['th']
    
    #保存
    df_us.to_csv(os.path.join(USER_PATH, str(QQ),'data.csv'))
    return 99

def send_err_msg(error):
    '''
    根据错误项返回错误信息
    '''
    if error == -1:
        return '好像出了奇怪的问题~请联系lc处理哦'
    elif error == 0:
        return "唔~你的等级还不够呢，努力提升等级吧"
    elif error == 1:
        return "ohno，你的铜不够了呢"
    elif error == 2:
        return "ohno，你的铅不够了呢"
    elif error == 3:
        return "ohno，你的钛不够了呢"
    elif error == 4:
        return "ohno，你的钍不够了呢"
    
