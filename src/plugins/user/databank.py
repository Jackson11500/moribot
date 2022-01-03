
service_list = {
    '图片':{'level':0,'cu':1,'pd':0,'ti':0,'th':0},
    '有人说':{'level':0,'cu':0,'pd':1,'ti':0,'th':0},
    '贴贴':{'level':0,'cu':0,'pd':0,'ti':0,'th':0},
    '传信':{'level':3,'cu':2,'pd':4,'ti':0,'th':0},
    
    '锁定背景':{'level':5,'cu':30,'pd':50,'ti':5,'th':0}
}

building = {
    'seperator' : {'lvreq':5, 'cu':150 ,'pd':50,'ti':15,'th':0, 'limit' : 1 , 'des':'分离机，可以实现钛与铜铅的转换，较低效率实现[钛-铜-铅]转换功能'},
    'disassembler' : {'lvreq':20, 'cu':500 ,'pd':500,'ti':100,'th':40, 'limit' : 1 , 'des':'解离机，可以实现钛与钍的转换，较低效率实现[钛-钍]转换功能'},
    
    'mass-driver' : {'lvreq':10, 'cu':100 ,'pd':200,'ti':20,'th':3, 'limit' : 1 , 'des':'质驱，与其他玩家交互实现资源发射与接受，解锁[转账]功能'},
    'launch-pad' : {'lvreq':15, 'cu':500 ,'pd':500,'ti':100,'th':20, 'limit' : 1 , 'des':'发射台，发射资源到其他区块，允许将资源投掷至其他玩家（不需要对方建造质驱），解锁[区块]并升级[转账]功能'},
    'interplanetary-accelerator' : {'lvreq':30, 'cu':2000 ,'pd':2000,'ti':400,'th':100, 'limit' : 1, 'des':'大型发射台，可以发射资源到其他星球，解锁[其他星球区块]'}
}

sector = {
    15 : {'name':'groundZero','cu':150 ,'pd':50,'ti':0,'th':0,'lagpro':5,'procu':1 ,'propd':1,'proti':0,'proth':0,'bonus':1},
    86 : {'name':'frozenForest ','cu':150 ,'pd':250,'ti':0,'th':0,'lagpro':8,'procu':2 ,'propd':2,'proti':0,'proth':0,'bonus':2}
}