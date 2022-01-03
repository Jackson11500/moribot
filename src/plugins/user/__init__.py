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

###每日重启
user_restart = on_command("数据备份",rule=endswith("数据备份"), priority=1, permission=SUPERUSER,block=True)

@user_restart.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    import src.plugins.user.user_data as us
    msg = us.backup()
    await bot.send(event=event,message=msg)
    await user_restart.finish("")
    
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
    
###锁定背景
user_lock_background = on_command("用户-锁定背景",permission=PRIVATE_FRIEND, priority=5,block=True)

@user_lock_background.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    from src.plugins.user.utils import check_service
    if check_service(event.user_id,'锁定背景')==0:
        await user_lock_background.finish("未绑定或等级不够！")
    if check_service(event.user_id,'锁定背景')!=99:
        await user_lock_background.finish("你的材料不够，请准备好材料后再来哦！")
    await bot.send(event=event,message='请发送图片，背景审核通过后即可使用！\n图片要求-能在一般的公开平台发布，不符合的图片将不允许通过哦（可以更换）')
    await bot.send_group_msg(group_id=180707407, message=f'{event.user_id}发起了锁定背景申请！')
    await user_lock_background.finish()
    
###锁定背景
user_transfer_base= on_command("转账：", priority=5,block=True)

@user_transfer_base.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    command = str(event.message).split('：')
    payer = str(event.user_id)
    receiver = command[0]
    type = command[1]
    amount = command[2]
    from src.plugins.user.utils import modify_single_res
    
    if not receiver.isdigit() or not amount.isdigit() or type not in ['cu','pd','ti','th']:
        await bot.send(event,message='请根据正确的格式转账！示例：\n用户-转账：12345678：cu：12\n分别填空：目标qq号，类型（cu/pd/ti/tu)，数量')
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