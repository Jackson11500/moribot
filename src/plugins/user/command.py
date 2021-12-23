'''
文本记录与阅读格式
[index],[para1]...[paran],[QQ],[time]
[index]=1:绑定  =2:[签到]
'''

'''
usedata:
index
QQ
注册时间
经验
是否已签到
变其他人猫娘次数
被变猫娘次数
今日签到经验
连续签到次数
'''
import os
import pandas as pd
import numpy as np

def save(us):
    ##save
    with open(main_folder+'userdata.csv','w') as file:
        for row in range(us.shape[0]):
            file.write(str(us[row,0]))
            for column in range(1,us.shape[1]):
                file.write(','+str(us[row,column]))
            file.write('\n')

#print('茉莉正在高速处理信息中...')
main_folder=os.getcwd()
main_folder2='D:/QQ/Bot/General分支(1.0.1)(1)/General分支(1.0.1)(1)/兔子-db包/用户数据/'
def user_sign_in(QQ):
    msg_box = "茉莉还在学习中，未连接到数据库！\n"
    us=pd.read_csv(main_folder2+'userdata.csv',skiprows=0,header=None).values
    for row in range(us.shape[0]):
        if us[row,1]!=QQ:
            continue
        if us[row,4]==3:    #7日奖励签到
            import random
            exp=random.randrange(1,11,1)       
            us[row,3]+=exp         
            if exp<2:
                msg_box+='快跑！！经验+'+str(exp)+'\n'
            elif exp<4:
                msg_box+='oh no 好像不妙，经验+'+str(exp)+'\n'
            elif exp<7:
                msg_box+='平平淡淡，经验+'+str(exp)+'\n'
            elif exp<10:
                msg_box+='吸吸吸，经验+'+str(exp)+'\n'
            elif exp==10:
                msg_box+='哇，茉莉也好想要这样的好运！经验+'+str(exp)+'\n'
            us[row,4]=1
        elif us[row,4]!=0:
            msg_box+='你今天已经签到过啦！还想偷偷再签一次？'+'\n'
            msg_box+='【今日已有{int(np.sum(us[:,4]))}人签到,大家的平均运气为{round(np.sum(us[:,7])/np.sum(us[:,4]),1)}】'+'\n'
        else:
            import random
            exp=random.randrange(1,11,1)
            us[row,3]+=exp
            us[row,4]=1
            us[row,7]=exp
            if exp<2:
                msg_box+='快跑！！经验+'+str(exp)+'\n'
            elif exp<4:
                msg_box+='oh no 好像不妙，经验+'+str(exp)+'\n'
            elif exp<7:
                msg_box+='平平淡淡，经验+'+str(exp)+'\n'
            elif exp<10:
                msg_box+='吸吸吸，经验+'+str(exp)+'\n'
            elif exp==10:
                msg_box+='哇，茉莉也好想要这样的好运！经验+'+str(exp)+'\n'
                #print('{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\+10.jpg}')

            us[row,8]+=1
            msg_box+='【已连续签到'+str(int(us[row,8]))+'天】'+'\n'
            if (us[row,8]%7==0):#7日奖励签到
                week=int(us[row,8])//7
                print('【已连续签到'+str(week)+'周,奖励可再签到一次，同时额外经验+'+str(week*3)+'】')
                us[row,3]+=week*3
                us[row,4]=3
                
            msg_box+=f'【今日已有{int(np.sum(us[:,4]))}人签到,大家的平均运气为{round(np.sum(us[:,7])/np.sum(us[:,4]),1)}】'+'\n'

            if np.sum(us[:,4])==1:
                us[row,3]+=5
                msg_box+='【作为今日第一名签到者，额外经验+5！】'+'\n'
            elif np.sum(us[:,4])==2:
                us[row,3]+=3
                msg_box+='【作为今日第二名签到者，额外经验+3！】'+'\n'
            elif np.sum(us[:,4])==3:
                us[row,3]+=1
                msg_box+='【作为今日第三名签到者，额外经验+1！】'+'\n'
        save(us)
    msg_box+='茉莉这里还没你的档案呢，要先注册才行哦'+'\n'
    return msg_box

def reboot():
    main_folder=os.getcwd()
    us=pd.read_csv(main_folder+'/userdata.csv',skiprows=0,header=None).values
    for row in range(us.shape[0]):
        if us[row,4]==0:
            us[row,8]=0
        us[row,4]=0
        us[row,7]=0

    ##save
    with open(main_folder+'/userdata.csv','w') as file:
        for row in range(us.shape[0]):
            file.write(str(us[row,0]))
            for column in range(1,us.shape[1]):
                file.write(','+str(us[row,column]))
            file.write('\n')

    return 'Fox News:茉莉的签到已重置'
#command=pd.read_csv(main_folder+'command_log.txt',header=None).values[-1,:]
#us=pd.read_csv(main_folder+'userdata.csv',skiprows=0,header=None).values
'''
if __name__ == "__main__":
    #注册系统
    if command[0]==0:
        row=0
        for row in range(us.shape[0]):
            if us[row,1]==command[1]:
                print('你已经注册过啦，还发。是想数据清空再注册一次吗')
                exit()

        us=np.row_stack((us,np.zeros((1,us.shape[1]))))
        us[row+1,:3]=[row+1,command[1],command[2]]
        print('{@,'+str(int(command[1]))+'}')
        print(f'注册成功！你是第{row+2}个成为我朋友的人，热烈欢迎')
        save()

    #个人信息系统
    elif command[0]==1:
        row=0
        for row in range(us.shape[0]):
            if us[row,1]==command[1]:
                print('检索资料库中...找到了!{@,'+str(int(command[1]))+'}，你的当前经验值为'+str(int(us[row,3])))
                print(f'你总共被变了{int(us[row,5])}次猫娘，同时将其他人变了{int(us[row,6])}次猫娘')
                exit()
        print(f'茉莉这里还没你的档案呢，要先注册才行哦')
        exit()

    #签到
    elif command[0]==2:

        for row in range(us.shape[0]):
            if us[row,1]==command[1]:
                print('{@,'+str(int(command[1]))+'}')
                if us[row,4]==3:    #7日奖励签到
                    import random
                    exp=random.randrange(1,11,1)       
                    us[row,3]+=exp         
                    if exp<2:
                        print('快跑！！经验+'+str(exp))
                    elif exp<4:
                        print('oh no 好像不妙，经验+'+str(exp))
                    elif exp<7:
                        print('平平淡淡，经验+'+str(exp))
                    elif exp<10:
                        print('吸吸吸，经验+'+str(exp))
                    elif exp==10:
                        print('哇，茉莉也好想要这样的好运！经验+'+str(exp))
                    us[row,4]=1
                elif us[row,4]!=0:
                    print(f'你今天已经签到过啦！还想偷偷再签一次？')
                    print(f'【今日已有{int(np.sum(us[:,4]))}人签到,大家的平均运气为{round(np.sum(us[:,7])/np.sum(us[:,4]),1)}】')
                else:
                    import random
                    exp=random.randrange(1,11,1)
                    us[row,3]+=exp
                    us[row,4]=1
                    us[row,7]=exp
                    if exp<2:
                        print('快跑！！经验+'+str(exp))
                    elif exp<4:
                        print('oh no 好像不妙，经验+'+str(exp))
                    elif exp<7:
                        print('平平淡淡，经验+'+str(exp))
                    elif exp<10:
                        print('吸吸吸，经验+'+str(exp))
                    elif exp==10:
                        print('哇，茉莉也好想要这样的好运！经验+'+str(exp))
                        print('{发送图片,D:\QQ\Bot\General分支(1.0.1)(1)\General分支(1.0.1)(1)\兔子-db包\娱乐\定向回复\+10.jpg}')

                    us[row,8]+=1
                    print('【已连续签到'+str(int(us[row,8]))+'天】')
                    if (us[row,8]%7==0):#7日奖励签到
                        week=int(us[row,8])//7
                        print('【已连续签到'+str(week)+'周,奖励可再签到一次，同时额外经验+'+str(week*3)+'】')
                        us[row,3]+=week*3
                        us[row,4]=3
                        
                    #print(f'【今日已有{int(np.sum(us[:,4]))}人签到')
                    print(f'【今日已有{int(np.sum(us[:,4]))}人签到,大家的平均运气为{round(np.sum(us[:,7])/np.sum(us[:,4]),1)}】')

                    if np.sum(us[:,4])==1:
                        us[row,3]+=5
                        print(f'【作为今日第一名签到者，额外经验+5！】')
                    elif np.sum(us[:,4])==2:
                        us[row,3]+=3
                        print(f'【作为今日第二名签到者，额外经验+3！】')
                    elif np.sum(us[:,4])==3:
                        us[row,3]+=1
                        print(f'【作为今日第三名签到者，额外经验+1！】')

                    
                    
                save()
                exit()
        print(f'茉莉这里还没你的档案呢，要先注册才行哦')
        exit()
        
    #表白
    elif command[0]==3:
        for row in range(us.shape[0]):
            if us[row,1]==command[1]:
                print('{@,'+str(int(command[1]))+'}')
                if us[row,4]==0:
                    print(f'茉莉不想理连每日打招呼都能忘记的人！')
                elif us[row,4]==2:
                    print(f'今后也要多多指教哦~')
                else:
                    us[row,3]+=10
                    us[row,4]=2
                    print(f'好哒好哒，一起来快乐玩耍吧~~ 经验+10！')
                save()
                exit()
        print(f'茉莉这里还没你的档案呢，要先注册才行哦')
        exit()

    #变猫娘
    elif command[0]==4:
        cat=['100%原生态','白猫','黑猫']
        cat_ct=['小妖怪','猫神','流浪中...','等待投喂']
        cat_touhou=['式神-橙','火焰猫燐']
        cat_nekopara=['巧克力','香草','枫','桂','红豆','椰子','水无月时雨']
        cat_nekoday=['小曼','小新','小露','艾尔莎']
        cat_mdt=['anuke','臭猫']
        import random
        cattype=random.choice(random.choice([cat,cat_ct,cat_nekopara,cat_touhou,cat_nekoday,cat_mdt]))
        if int(command[3])==0:
            print('{@,'+str(int(command[1]))+'}',end=' ')
            print(f'使用了猫娘变化大法，结果一不小心把自己变成了猫娘[{cattype}]，大家快来玩弄她吧',end=' ')
            for row in range(us.shape[0]):
                if us[row,1]==command[1]:
                    us[row,5]+=1
                    us[row,6]+=1
        elif int(command[1])==int(command[2]):
            print('{@,'+str(int(command[1]))+'}',end=' ')
            print(f'将自己变成了猫娘[{cattype}]!')
            for row in range(us.shape[0]):
                if us[row,1]==command[1]:
                    us[row,5]+=1
                    us[row,6]+=1
        else:
            for row in range(us.shape[0]):
                if us[row,1]==command[1]:
                    us[row,5]+=1
                    print('{@,'+str(int(command[2]))+'}',end=' ')
                    print('被',end=' ')
                    print('{@,'+str(int(command[1]))+'}',end=' ')
                    print(f'变成了猫娘[{cattype}]!')
                if us[row,1]==command[2]:
                    us[row,6]+=1
        save()        
        exit()

    elif command[0]==5:
        print('---猫娘统计表---')

        data_a=us[np.argsort(us[:,5])]
        print('{mid,{取群成员信息,{var,'+str(int(data_a[-2,1]))+'}},昵称:,;}',end='')
        print(f'位居猫娘乐园宝座！总共被变了{data_a[-2,5]}次猫娘！')
        print('{mid,{取群成员信息,{var,'+str(int(data_a[-3,1]))+'}},昵称:,;}',end='')
        print(f'是猫娘王国丞相，总共被变了{data_a[-3,5]}次猫娘！')    

        data_b=us[np.argsort(us[:,5])]
        print('{mid,{取群成员信息,{var,'+str(int(data_b[-2,1]))+'}},昵称:,;}',end='')
        print(f'位居狗子队宝座！总共将{data_b[-2,5]}人变成了猫娘！')
        print('{mid,{取群成员信息,{var,'+str(int(data_b[-3,1]))+'}},昵称:,;}',end='')
        print(f'是狗子队丞相，总共将{data_b[-3,5]}人变成了猫娘！')
        
        exit()
        
        
    '''