def isallow(group,level):#检验许可
    import numpy as np
    if np.load('D://QQ//Bot//nonebot//moribot//src//plugins//group_status.npy',allow_pickle=True).item()[group]<level:
        return False
    else: 
        return True