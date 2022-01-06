# import nonebot
from nonebot import get_driver

global_config = get_driver().config

from nonebot import on_command,on_regex
from nonebot.rule import endswith, to_me,startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER

from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment

from src.plugins.__toolbox import checkallow
from nonebot.adapters.cqhttp import PRIVATE_FRIEND

from configs.path_config import PLUGINS_PATH
import os
THIS_PATH = os.path.join(PLUGINS_PATH,'user')

###每日重启
user_restart = on_command("数据备份",rule=endswith("数据备份"), priority=1, permission=SUPERUSER,block=True)

@user_restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.user_data as us
    msg = us.backup()
    await bot.send(event=event,message=msg)
    us.combine_user_data()
    us.ranking_list()
    await bot.send(event=event,message="排行榜已刷新")
    await user_restart.finish()
    
###签到
user_signin = on_command("签到",rule=endswith("签到"), priority=3,block=True)
@user_signin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'user')==0:
        await user_signin.finish()
    import src.plugins.user.user_data as us
    text = await us.user_sign_in(bot=bot, event=event, state=state)
    import os 
    if (os.path.exists(text)):
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+MessageSegment.image(file = "file:///"+text))
    else:
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+text)
    await user_signin.finish()

###注册
user_register = on_command("注册",rule=endswith("注册"), priority=3,block=True)

@user_register.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'user')==0:
        await user_register.finish()
    import src.plugins.user.user_data as us
    par = us.register(event.user_id)
    if par==0:
        msg = MessageSegment.reply(event.message_id)+"茉莉这里已经有你的档案啦，不需要再注册一遍的！"
    else:
        msg = MessageSegment.reply(event.message_id)+f"注册成功！你是第{par}位成为茉莉朋友的人！"
    await bot.send(event=event,message=msg)
    await user_register.finish()

###注册
user_register = on_command("排行榜",rule=endswith("排行榜"), priority=5,block=True)

@user_register.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'user')==0:
        await user_register.finish()
    import src.plugins.user.user_data as us
    #us.ranking_list()
    msg = MessageSegment.reply(event.message_id)+MessageSegment.image(file = "file:///"+os.path.join(THIS_PATH,'ls_image','ranking_list.jpg'))
    await bot.send(event=event,message=msg)
    await user_register.finish()

###交易
user_register = on_command("交易",rule=endswith("交易"), priority=3,block=True)

@user_register.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'user')==0:
        await user_register.finish()
    msg='欢迎来到茉莉的临时交易所，现在提供的服务如下：\n\
输入指令即可查询功能使用方式\n\
1.随机图片    造价1cu\n\
2.有人说    造价1pd\n\
3.传信  造价2cu4pd，需要3级\n\
4.转账  3级后解锁初级转账（将资源投掷在对面基地），投掷过程会损失一半的资源\n\
转账是目前唯一获取不同资源的手段，茉莉也在努力研发熔炉、质驱和发射台，玩家解锁后可以以更低的损耗实现资源转换|转账\n\
5.锁定背景  5级，30cu50pd5ti，锁定一个自定义图片作为签到背景\n\
更完善的交易所正在建造中，敬请期待'
    await bot.send(event=event,message=msg)
    await user_register.finish()

###锁定背景
user_lock_background = on_command("锁定背景", priority=5,block=True)

@user_lock_background.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    from src.plugins.user.utils import check_service
    if check_service(event.user_id,'锁定背景')==0:
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+"未绑定或等级不够！")
        await user_lock_background.finish()
    elif check_service(event.user_id,'锁定背景')!=99:
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+"你的材料不够，请准备好材料后再来哦！")
        await user_lock_background.finish()
    else:
        await bot.send(event=event,message=MessageSegment.reply(event.message_id)+'请私聊茉莉发送图片，背景审核通过后即可使用！\n图片要求-能在一般的公开平台发布，不符合的图片将不允许通过哦（可以更换）\n长宽比应尽可能接近10:6')
        await bot.send_group_msg(group_id=180707407, message=f'{event.user_id}发起了锁定背景申请！')
        await user_lock_background.finish()
    
###锁定背景
user_transfer_base= on_command("转账",rule = endswith('转账'),priority=7,block=True)

@user_transfer_base.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    if checkallow(event,'user')==0:
        await user_register.finish()
    msg='在玩家达到3级后，可以将资源投掷到别人基地\n\
这是最原始的转账方式，过程中会损失大量的资源(约50%)\n\
转账格式：\n\
转账：[对方QQ]：[项目]：[数量]\n\
实例：\n\
转账：12345678：cu：100\n\
目前项目包括：cu、pd、ti、th(铜铅钛钍)\n\
据说中后期的玩家们常常会用质驱、发射台甚至载荷驱动塔进行大规模高效率交易，想必资源损耗会少很多吧\n\
转账记录会被存档并定期检查，如果发现用小号收集资源会给予惩罚哦~'
    await bot.send(event=event,message=msg)
    await user_register.finish()

user_transfer_base= on_command("转账：", priority=8,block=True)

@user_transfer_base.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    command = str(event.message).split('：')
    payer = str(event.user_id)
    receiver = command[0]
    type = command[1]
    amount = command[2]
    from src.plugins.user.utils import modify_single_res
    
    if not receiver.isdigit() or not amount.isdigit() or type not in ['cu','pd','ti','th'] or int(amount)<=0:
        await bot.send(event,message='请根据正确的格式转账！示例：\n转账：12345678：cu：12\n分别填空：目标qq号，类型（cu/pd/ti/tu)，数量')
        await user_transfer_base.finish()
    
    if modify_single_res(int(payer))==99 and modify_single_res(int(receiver))==99:
        if modify_single_res(int(payer),level = 3, amount = -int(command[2]),res_type=type)==99:
            if modify_single_res(int(receiver),level = 3, amount = int(int(command[2])/2),res_type=type)==99:
                await bot.send(event,message='你已成功向对面核心投掷资源！\n如果想要更高的转账效率，来尝试建造质驱或发射台吧！')
                await user_transfer_base.finish()
            else:
                modify_single_res(int(payer),level = 3, amount = int(command[2]),res_type=type)
                await bot.send(event,message='转账失败！对方核心还不能接收这么多的资源，资源已退回。\n(对方等级太低无法转账，防止小号)')
                await user_transfer_base.finish()
        else:
            await bot.send(event,message='转账失败，你的等级或材料不够！')
            await user_transfer_base.finish()
    else:
        await bot.send(event,message='用户数据读取失败！')
        await user_transfer_base.finish()
        
###成就:图片收藏家
user_register = on_command("添加成就-图片收藏家：",permission=SUPERUSER, priority=5,block=True)

@user_register.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    command = str(event.message).split('：')
    id = command[0]
    count = command[1]
    
    import src.plugins.user.achievement as ach
    ach.add_achievement(int(id),ach_name = '图片收藏家',level = int(count),one_cu = int(count)//10,one_pd = int(count)//10,bonus = int(count)//100)
    msg = f'已成功为{id}添加永久成就：图片收藏家({int(count)})'
    msg += f'\n获得奖励：铜+{int(count)//10},铅+{int(count)//10}'
    msg += f'\nbonus+{int(count)//100}'
    await bot.send(event=event,message=msg)
    await user_register.finish()
