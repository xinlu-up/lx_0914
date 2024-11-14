import requests
from client.lark_project_client import LarkClientSingleton
# from api.work_item_info import update_work_items_by_id
import json
import logging
import time
from typing import List
from feishu_api import *
from feishu_utils.feishu_message import FeishuMessage
from feishu_utils.feishu_sheets import FeishuSheets
import requests
import sys
import ast
import schedule


def seed_message(message,id):
    """
    :type message: str
    :type id :int
    """    
    # 我要通过这个id获取是谁创建的
    # 根据id获取所有的解析文件，然后获得创建者，然后或者创建者id,然后发消息。id 是email。
    # 现在默认的都是写死的，都是发给我
    interactive = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**：{message}**\n",
                            "tag": "lark_md"
                        }
                    } 
                ],
                "tag": "div"
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": f" 需求文档报警 ",
                "tag": "plain_text"
            }
        }
    }
    logging.info("已经收到该报警消息")
    jira_list = ['<at email=xin.lu2.o@nio.com></at>']
    # jira_list = ['<at id=all>所有人</at>']
    FM = FeishuMessage()
    FM.message({'type': 'open_id', 'id': 'ou_b508c318c64f780f1ad98cd8015a2557'},'interactive',interactive) # 个人   lx
    FM.message({'type': 'open_id', 'id': 'ou_f3998ad462a4792c79f9f6a96f4fd68c'},'interactive',interactive) # 个人   ou_f3998ad462a4792c79f9f6a96f4fd68c
    # FM.message({'type': 'open_id', 'id': 'ou_7244c2da2e0edaa99d353804767c7524'},'interactive',interactive)
    # FM.message({'type': 'chat_id', 'id': 'oc_218929f9da3f156359f451395254faaa'},'interactive',interactive) # 群聊

def delete_name(name2):
    with open('test0718.txt','r') as task:
        lines_to_keep = [line for line in task if name2 not in line]  
        print(lines_to_keep)
    task.close()
    
    with open('test0718.txt','w') as task1:
        for line in lines_to_keep:
            task1.writelines(line)
    task1.close()  
    
            
            
if __name__ == "__main__":
    
    # with open('submitted_task.txt','r') as task1:
    #     for line in task1:
    #         if line == '\n':
    #             print("uyoiu")
    #             continue
    #         print(line)
    # task1.close
    seed_message('hello',1)
    
    
    