import sys
sys.path.append("..") 

url = "https://mdt.wayzer.top/api/servers/list"

firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

import json
from urllib.request import Request, urlopen
import pandas as pd

def get_server():
    #构建请求
    request = Request(url, headers=firefox_headers )
    html = urlopen( request )
    #获取数据
    data = html.read()
    #转换成字典数据
    data_json = json.loads(data)
    server = pd.DataFrame(data_json).sort_values(by = ['players'])
    return server

def get_server_msg(bot,event):
    server = get_server()
    
    msg_list = []
    sender = {
    "type": "node",
    "data": {
        "id":str(event.message_id)
    },
    }
    msg_list.append(sender)
    source_data = {
    "type": "node",
    "data": {
        "name": f"无所不知茉莉酱",
        "uin": f"{bot.self_id}",
        "content": f"当前大家都在哪个服玩呢？",
    },
    }
    msg_list.append(source_data)
    
    count = 0
    for s in range(len(server)):
        if server.loc[s,'players'] == 0: 
            break
        
        startindex = -1
        index = -1
        while (index < len(server.loc[s,'name']) - 1):
            index += 1
            if server.loc[s,'name'][index] == '[':
                startindex = index 
            elif server.loc[s,'name'][index] == ']' and startindex!=-1:
                new_str = ""
                for j in range(len(server.loc[s,'name'])):
                    if j >= startindex and j <= index:
                        continue
                    new_str += server.loc[s,'name'][j]
                    
                server.loc[s,'name'] = new_str
                startindex = -1 
                index = -1
            
        count += 1
        data = {
        "type": "node",
        "data": {
            "name": f"{server.loc[s,'name']}の茉莉酱",
            "uin": f"{bot.self_id}",
            "content": f"玩家人数：{server.loc[s,'players']}\nip：{server.loc[s,'address']}\n地图：{server.loc[s,'mapName']}\n模式：{server.loc[s,'mode']}\n波次：{server.loc[s,'wave']}",
        },
        }
        msg_list.append(data)
    
    source_data = {
    "type": "node",
    "data": {
        "name": f"无所不知茉莉酱",
        "uin": f"{bot.self_id}",
        "content": f"来源：https://mdt.wayzer.top/v2/server",
    },
    }
    msg_list.append(source_data)
    return msg_list