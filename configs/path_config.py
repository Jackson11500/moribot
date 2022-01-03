from pathlib import Path

#主目录
MAIN_PATH = str(Path(".").absolute())
#插件目录
PLUGINS_PATH = str(Path("./src/plugins").absolute())
# 字体路径
FONT_PATH = str(Path("resources/fonts").absolute())
# 图片路径
IMAGE_PATH = str(Path("resources/img").absolute())
# 用户数据路径
USER_PATH = str(Path("data/userdata").absolute())


'''
def init_path():
    global USER_PATH,IMAGE_PATH
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    USER_PATH.mkdir(parents=True, exist_ok=True)
    
    
    IMAGE_PATH = str(IMAGE_PATH.absolute())
    DATA_PATH = str(USER_PATH.absolute())
    
    
init_path()
'''