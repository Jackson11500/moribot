def isallow(event,level):#检验许可
    import numpy as np
    try:
        if np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()[event.group_id]<level:
            return False
        else: 
            return True
    except KeyError:
        return True
    
def checkallow(event,name):
    '''
    检验群组权限\n
    group_name,intro,hidden,chatting,intergroup,little_game,mdt,random_pic,someone_say,technique,user
    '''
    from configs.path_config import PLUGINS_PATH
    import pandas as pd
    import os
    group_status=pd.read_csv(os.path.join(PLUGINS_PATH,'group_status.csv'), index_col=0)
    return int(group_status.loc[str(event.group_id),name])