def process_code():
    """
    源码-->源码片段并用于查询
    """
    
    source_mainfolder = "D://QQ//Bot//mdt-数据//"
    import os
    processtype=['Blocks','Bullets','Items','Liquids','Planets','SectorPresets','StatusEffects','UnitTypes','Weathers']
    source_folder = sorted(os.listdir(source_mainfolder+'content' ))
    random=0

    for file in source_folder:
        if file[:-5] not in processtype:
            continue
        print(file)
        print(file)
        f = open(source_mainfolder+f'content//{file}','r')
        file=file[:-5]

        #开始读文件
        filelist=''     #list类
        filetro=''      #type类
        readindex=0     #index=1:开始阅读list类
        
        filename=''     #初始化filename
        filestorage=''  #初始化filestorage
        start=0
        for line in f.readlines():
            #读取list
            if readindex==0:
                if f'public class {file}' in line:
                    filelist+=line+'\n'
                    start=1
                    continue
                elif '@Override' in line:
                    readindex=1
                    with open(source_mainfolder+f'data//{file}','w') as fl:
                        fl.write(filelist)
                    continue
                elif start==1:
                    filelist+=line+'\n'
            #读取type
            elif readindex==1:
                if len(line)>9 and line[9]!=' ' and ' = new ' in line:
                    #保存上一轮
                    if filename!='':
                        with open(source_mainfolder+f'type//{filename}','w') as fn:
                            fn.write(filestorage)
                        with open(source_mainfolder+f'ran//{random}','w') as fn:
                            fn.write(filestorage)
                        random+=1
                    #进行下一轮
                    filestorage=''
                    filename=line.find('=')
                    filename=line[8:filename-1]
                    filestorage+=line+'\n'
                elif line.startswith('}'):
                    #保存上一轮
                    with open(source_mainfolder+f'type//{filename}'.lower(),'w') as fn:
                        fn.write(filestorage)
                    with open(source_mainfolder+f'ran//{random}'.lower(),'w') as fn:
                        fn.write(filestorage)
                    break                
                else:
                    filestorage+=line+'\n'
                    
def ran_ques():
    """
    源码-->源码属性并用在随机问题测试
    """
    source_folder = "D://QQ//Bot//mdt-数据//"
    import os
    processtype=['Blocks','Bullets','Items','Liquids','Planets','SectorPresets','StatusEffects','UnitTypes','Weathers']
    source_folder = sorted(os.listdir(source_folder+'content' ))
    random=0

    for file in source_folder:
        if file[:-5] not in processtype:
            continue
        if 1:
            f = open(source_folder+f'content//UnitTypes.java','r')
            file=file[:-5]
            print(file)

            #开始读文件
            filename=''     #初始化filename
            filestorage=''  #初始化filestorage
            for line in f.readlines():
                if len(line)>9 and line[9]!=' ' and ' = new ' in line:
                    #进行下一轮
                    filestorage=''
                    filename=line.find('=')
                    filename=line[8:filename-1]
                    filestorage+=line+'\n'
                elif 'speed = ' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_speed','w') as fn:
                        sindex=line.find('=')
                        dindex=line.find('f;')
                        fn.write(line[sindex+2:dindex])  
                elif 'armor = ' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_armor','w') as fn:
                        sindex=line.find('=')
                        dindex=line.find('f;')
                        fn.write(line[sindex+2:dindex])           
                elif 'buildSpeed = ' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_buildSpeed','w') as fn:
                        sindex=line.find('=')
                        dindex=line.find('f;')
                        fn.write(line[sindex+2:dindex])      
                elif 'health = ' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_health','w') as fn:
                        sindex=line.find('=')
                        dindex=line.find(';')
                        fn.write(line[sindex+2:dindex])    
                elif 'AmmoType' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_ammo','w') as fn:
                        if 'Power' in line:
                            fn.write('power') 
                        else:
                            sindex=line.find('s.')
                            ammoname=''
                            i=0
                            while i<11:
                                if line[sindex+2+i]==',' or line[sindex+2+i]==')':
                                    break
                                ammoname+=line[sindex+2+i]
                                i+=1
                            fn.write(ammoname)              
                elif 'weapons.add' in line:
                    filename='block'
                
                elif line.startswith('}'):
                    break                
        
        if 1:
            f = open(source_folder+f'content//Blocks.java','r')
            file=file[:-5]
            print(file)

            #开始读文件
            filename=''     #初始化filename
            filestorage=''  #初始化filestorage
            size=1
            wallHealthMultiplier=4
            for line in f.readlines():
                if len(line)>9 and line[9]!=' ' and ' = new ' in line:
                    #进行下一轮
                    filestorage=''
                    filename=line.find('=')
                    filename=line[8:filename-1]
                    filestorage+=line+'\n'
                elif 'size = ' in line:
                    sindex=line.find('=')
                    dindex=line.find(';')
                    size=int(line[sindex+2:dindex])
    
                elif 'health = ' in line:
                    with open(source_folder+f'exam//ran_source//{filename}_health','w') as fn:
                        sindex=line.find('=')
                        dindex=line.find(';')
                        fn.write( str(eval(line[sindex+2:dindex])) )

                elif line.startswith('}'):
                    break                

def exam_gen():
    #源码属性-->随机问题
    import os

    main_folder="D://QQ//Bot//mdt-数据//"
    source_folder = sorted(os.listdir(main_folder+'exam/ran_source' ))
    random=0
    #print(source_folder)
    #print(len(source_folder))
    import random

    with open(main_folder+'/log/ans_record','w') as f:
        f.write('')

    while True:
        print('嘻嘻，有勇气来挑战哦~那就由茉莉给你出道随机源码测试题吧。')
        ranseed=random.randrange(1,len(source_folder),1)
        index_=source_folder[ranseed].find('_')
        unittype=source_folder[ranseed][:index_]
        questtype=source_folder[ranseed][index_+1:]
        print(f'whats the {questtype} of {unittype}?')
        print(f'请问{unittype}的{questtype}属性为:')
        f=open(main_folder+f'exam/ran_source/{source_folder[ranseed]}','r')
        ans=f.readlines()[0]
        if ans.endswith('f'):
            ans=ans[:-1]
        #print(ans)
        if unittype!='block':
            break
    ans_dic=['A','B','C','D']

    def write_ans(ans):
        with open(main_folder+'/log/answer','w') as f:
            f.write(ans)

    if questtype=='armor':
        ans=int(ans)
        ans_list=[ans-3,ans-2,ans-1,ans+1,ans+2,ans+3]
        random.shuffle(ans_list)
        #print(ans_list)
        ans_list=[ans,ans_list[0],ans_list[1],ans_list[2]]
        random.shuffle(ans_list)
        #print(ans_list)
        print(f'A={ans_list[0]}, B={ans_list[1]}, C={ans_list[2]}, D={ans_list[3]}')
        write_ans(f'正确答案是  {ans_dic[ans_list.index(ans)]}: {ans}')

    elif questtype=='buildSpeed':
        ans=float(ans)
        ans_int=max(int(ans*10)/100,0.1)
        ans_list=[ans-3*ans_int,ans-2*ans_int,ans-1*ans_int,ans+1*ans_int,ans+2*ans_int,ans+3*ans_int]
        random.shuffle(ans_list)
        ans_list=[ans,round(ans_list[0],2),round(ans_list[1],2),round(ans_list[2],2)]
        random.shuffle(ans_list)
        print(f'A={ans_list[0]}, B={ans_list[1]}, C={ans_list[2]}, D={ans_list[3]}')
        write_ans(f'正确答案是  {ans_dic[ans_list.index(ans)]}: {ans}')

    elif questtype=='speed':
        ans=float(ans)*7.5
        ans_int=ans*1/5
        ans_list=[ans-3*ans_int,ans-2*ans_int,ans-1*ans_int,ans+1*ans_int,ans+2*ans_int,ans+3*ans_int]
        random.shuffle(ans_list)
        ans=round(ans,2)
        ans_list=[ans,round(ans_list[0],2),round(ans_list[1],2),round(ans_list[2],2)]
        random.shuffle(ans_list)
        print(f'A={ans_list[0]}, B={ans_list[1]}, C={ans_list[2]}, D={ans_list[3]}')
        write_ans(f'正确答案是  {ans_dic[ans_list.index(ans)]}: {ans}')

    elif questtype=='health':
        ans_int=10**(len(ans)-3)*5 if int(ans[0])<5 else 10**(len(ans)-1)
        ans=int(ans)
        ans_list=[ans-3*ans_int,ans-2*ans_int,ans-1*ans_int,ans+1*ans_int,ans+2*ans_int,ans+3*ans_int]
        random.shuffle(ans_list)
        ans_list=[ans,ans_list[0],ans_list[1],ans_list[2]]
        random.shuffle(ans_list)
        print(f'A={ans_list[0]}, B={ans_list[1]}, C={ans_list[2]}, D={ans_list[3]}')
        write_ans(f'正确答案是  {ans_dic[ans_list.index(ans)]}: {ans}')

    elif questtype=='ammo':
        #print(ans)
        ans_list=['power','coal','graphite','thorium']
        '''
        ans_list.remove(ans)
        random.shuffle(ans_list)
        ans_list[0]=ans
        random.shuffle(ans_list[:3])
        '''

        print(f'A={ans_list[0]}, B={ans_list[1]}, C={ans_list[2]}, D={ans_list[3]}')
        write_ans(f'正确答案是  {ans_dic[ans_list.index(ans)]}: {ans}')

    print('请在15秒内回答，只需回复A/B/C/D就可以啦')
    
def exam_feedback():
    '''
    反馈答题结果
    '''

    import pandas as pd
    import numpy as np

    main_folder='D:/QQ/Bot/General分支(1.0.1)(1)/General分支(1.0.1)(1)/兔子-db包/mdt-数据/'

    result=pd.read_csv(main_folder+'/log/ans_record',header=None).values
    Row=result.shape[0]
    Q_list=[]
    rs=[0,0,0,0]
    rs_dic={'A':0,'B':1,'C':2,'D':3}
    for row in range(Row):
        if result[Row-row-1,0] in Q_list:
            result[Row-row-1,1]=''
            continue
        if result[Row-row-1,1] in ['A','B','C','D']:
            rs[rs_dic[result[Row-row-1,1]]]+=1
            Q_list.append(result[Row-row-1,0])
        

    fias=f'本轮答题结束，各选项支持人数如下：A：{rs[0]}，B：{rs[1]}，C：{rs[2]}，D：{rs[3]}'
    print(fias)
    with open(main_folder+'/log/answer','r') as f:
        print(f.read())
    with open(main_folder+'/log/ans_record','w') as f:
        f.write('')

process_code()