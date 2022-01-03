from nonebot.adapters.cqhttp.permission import GROUP
#from utils.image_utils import get_img_hash
import random
#from utils.message_builder import image
from nonebot import on_message
from utils.utils import get_message_text, get_message_imgs
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
#from utils.http_utils import AsyncHttpx
#from utils.manager import group_manager



__zx_plugin_name__ = "复读"
__plugin_usage__ = """
usage：
    重复3次相同的消息时会复读
""".strip()
__plugin_des__ = "群友的本质是什么？是复读机哒！"
__plugin_type__ = ("其他",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"fudu": "复读"}
__plugin_configs__ = {
    "FUDU_PROBABILITY": {"value": 0.7, "help": "复读概率", "default_value": 0.7}
}

from src.plugins.__toolbox import isallow

class Fudu:
    def __init__(self):
        self.data = {}

    def append(self, key, content):
        self._create(key)
        self.data[key]["data"].append(content)

    def clear(self, key):
        self._create(key)
        self.data[key]["data"] = []
        self.data[key]["is_repeater"] = False

    def size(self, key) -> int:
        self._create(key)
        return len(self.data[key]["data"])

    def check(self, key, content) -> bool:
        self._create(key)
        return self.data[key]["data"][0] == content

    def get(self, key):
        self._create(key)
        return self.data[key]["data"][0]

    def is_repeater(self, key):
        self._create(key)
        return self.data[key]["is_repeater"]

    def set_repeater(self, key):
        self._create(key)
        self.data[key]["is_repeater"] = True

    def _create(self, key):
        if self.data.get(key) is None:
            self.data[key] = {"is_repeater": False, "data": []}


_fudu_list = Fudu()


fudu = on_message(permission=GROUP, priority=50)


@fudu.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not isallow(event,2):
        await fudu.finish()
        
    if get_message_text(event.json()):
        if get_message_text(event.json()).find("@小狐狸茉莉") != -1:
            await fudu.finish("复制粘贴的虚空艾特？", at_sender=True)
    imgs = get_message_imgs(event.json())
    msg = get_message_text(event.json())
    if not imgs and not msg:
        return
    if imgs:
        return
        img_hash = await get_fudu_img_hash(imgs[0], event.group_id)
    else:
        img_hash = ""
    add_msg = msg + "|-|" + img_hash
    if _fudu_list.size(event.group_id) == 0:
        _fudu_list.append(event.group_id, add_msg)
    elif _fudu_list.check(event.group_id, add_msg):
        _fudu_list.append(event.group_id, add_msg)
    else:
        _fudu_list.clear(event.group_id)
        _fudu_list.append(event.group_id, add_msg)
    if _fudu_list.size(event.group_id) > 2:
        #if random.random() < 0.5 and not _fudu_list.is_repeater(event.group_id):
        if not _fudu_list.is_repeater(event.group_id):
            repeatlist=["打断施法！","破案啦，你群全是复读机","什么事什么事这么好玩呢，茉莉也想看看~"]
            if random.random() < 1-1/float(len(repeatlist)):
                await fudu.finish(random.choice(repeatlist))
            _fudu_list.set_repeater(event.group_id)
            if imgs and msg:
                return 0
                rst = msg + image(f"compare_{event.group_id}_img.jpg", "temp")
            elif imgs:
                return 0
                rst = image(f"compare_{event.group_id}_img.jpg", "temp")
            elif msg:
                rst = msg
            else:
                rst = ""
            if rst:
                await fudu.send(rst)

'''
|打断复读！！！
|破案啦，你群全是复读机
|什么事什么事这么好玩呢，茉莉也想看看~
|{偷偷禁言一个复读姬，应该没什么问题吧{禁言,{QQ},60}}
async def get_fudu_img_hash(url, group_id):
    try:
        if await AsyncHttpx.download_file(
            url, IMAGE_PATH + f"temp/compare_{group_id}_img.jpg"
        ):
            img_hash = get_img_hash(IMAGE_PATH + f"temp/compare_{group_id}_img.jpg")
            return str(img_hash)
        else:
            logger.warning(f"复读下载图片失败...")
    except Exception as e:
        logger.warning(f"复读读取图片Hash出错 {type(e)}：{e}")
        return ""
'''