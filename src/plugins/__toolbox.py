def isallow(event,level):#检验许可
    import numpy as np
    if np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()[event.group_id]<level:
        return False
    else: 
        return True