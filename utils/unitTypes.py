import numpy as np
from configs.path_config import IMAGE_PATH
import os

'''
class unittype:
    def __init__(self,name:int,type:int,tier:int):
        self.name = name
        self.type = type
        self.tier = tier
    
    def ui_image_path(self):
        return os.path.join(IMAGE_PATH,'mdt','ui','unit-'+self.name+'-ui.png')
'''
    
UNIT_CORE = [['alpha', 'beta', 'gamma'],
            ['evoke', 'incite', 'emanate']]

UNIT_PRO =  [['dagger','mace','fortress','scepter','reign'],
            ['nova','pulsar','quasar','vela','corvus'],
            ['crawler','atrax','spiroct','arkyid','toxopid'],
            ['risso','minke','bryde','sei','omura'],
            ['retusa','oxynoe','cyerce','aegires','navanax'],
            ['flare','horizon','zenith','antumbra','eclipse'],
            ['mono','poly','mega','quad','oct'],
            ['stell','locus','precept','vanquish','conquer'],
            ['merui','cleroi','anthicus','tecta','collaris'],
            ['elude','avert','obviate','quell','disrupt']]

UNIT_PRO_NP = np.array(UNIT_PRO)          
UNIT_CORE_NP = np.array(UNIT_CORE)     

def unit_types(array, i, type_first: bool):
    '''
    type_first = true:先排兵种再排等级
    type_first = false:先排等级再排兵种
    '''
    if i>array.size:
        raise ValueError("超出矩阵限制")
    if type_first:
        return array[i // array.shape[0],i % array.shape[0]]
    else:
        return array[i % array.shape[0],i // array.shape[0]]

def all_unit_types(i: int, type_first: bool) -> str:
    '''
    先返回core再返回其他
    type_first = true:先排兵种再排等级
    type_first = false:先排等级再排兵种
    '''
    if i<0 or i>UNIT_CORE_NP.size + UNIT_PRO_NP.size:
        raise ValueError("unit types>0")
    if i<UNIT_CORE_NP.size:
        return unit_types(UNIT_CORE_NP,i,type_first)
    else:
        return unit_types(UNIT_PRO_NP,i-UNIT_CORE_NP.size,type_first)
    
def ui_image_path_unit(unit:str) -> str:
    return ui_image_path('unit',unit)

def ui_image_path(type:str,unit:str) ->str:
    return os.path.join(IMAGE_PATH,'mdt','ui',f'{type}-{unit}-ui.png')

def all_unit_image(i: int, type_first: bool) -> str:
    return ui_image_path_unit(all_unit_types(i,type_first))