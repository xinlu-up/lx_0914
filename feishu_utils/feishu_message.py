#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Feishu Message Client"""
import datetime
import json
import os
import requests

user_name_to_open_id = {
        "jie.shan": "jie.shan@nio.com",
        "Shipei TIAN": "ou_87bcbd343b915ff2e22605fe88aca141",
        "ronnie.zhao": "ronnie.zhao@nio.com",
        "BadaXIN": "bada.xin@nio.com",
        "pony.pan": "pony.pan@nio.com",
        "Kai ZHANG": "ou_a6c12c3b75bd004d34bc0758bc71ad96",
        "shibo.shang": "shibo.shang@nio.com",
        "xinxing.chen1": "xinxing.chen1@nio.com"
    }

class FeishuMessage:
    _FEISHU_HOST = 'https://open.feishu.cn/open-apis'


    def __init__(self):
        token_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config',
                                  'parking_test_token.json')
        if not os.path.exists(token_file):
            print('Feishu message init failed and parking_test_token.json not exist')
            self._headers = None
            return
        with open(token_file, 'r+') as auth_file:
            token_info = json.load(auth_file)
        self._app_secret = {
            'app_id': token_info.get('feishu_app_id'),
            'app_secret': token_info.get('feishu_app_secret')
        }
        self._access_token = self.get_tenant_access_token()
        self._headers = {
            'Authorization': 'Bearer {}'.format(self._access_token),    # 't-g10479i4J7CFUGFVJWI6H4ULO3KFGY4KPGQWBWLX'
            'Content-Type': 'application/json; charset=utf-8'
        }

    def get_tenant_access_token(self):
        """get tenant access token by app_id and app_secret"""
        url = '{}/auth/v3/tenant_access_token/internal'.format(self._FEISHU_HOST)
        res = requests.post(url, data=self._app_secret)
        print(res.json())
        if res.status_code == 200:
            res = res.json()
            return res.get('tenant_access_token', None)
        return None

    def message(self, id, msg_type, content):
        '''
        群聊或个人单发消息
        :param id: {'type':id类型, 'id': id} 如群聊： {'type':'chat_id', 'id':'oc_4161de2f30c71a9cc35aa4e52220'}
        :param content & msg_type: 详见https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json#11e75d0
        :return: res['msg']
        '''
        url = '{}/im/v1/messages?receive_id_type={}'.format(self._FEISHU_HOST, id['type'])
        # 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id'
        email = list()
        data = {
            "receive_id": id['id'],
            "content": json.dumps(content),
            "msg_type": msg_type
        }
        res = requests.post(url, headers=self._headers, data=json.dumps(data))     # 这个地方失败了
        print(res.json())
        if res.status_code == 200:
            res = res.json()
            return res.get('msg')
        return None

    def batch_message(self, ids, msg_type, content):
        '''
        批量发送消息
        :param ids: ids为list()类型
        :param msg_type & content: 文档地址：https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
        :return: res
        '''
        url = '{}/message/v4/batch_send/'.format(self._FEISHU_HOST)
        ids['msg_type'] = msg_type
        content_type = 'card' if msg_type == 'interactive' else 'content'
        ids[content_type] = content
        res = requests.post(url, headers=self._headers, data=json.dumps(ids))
        print(res.json())
        if res.status_code == 200:
            res = res.json()
            return res
        return None

    def get_chat_id(self):
        url = '{}/im/v1/chats'.format(self._FEISHU_HOST)
        res = requests.get(url, headers=self._headers)
        print(res.json())
        if res.status_code == 200:
            res = res.json()
            return res.get('data')
        return None

def main():
    jira_list = ['NT2ADD-5000 <at email=bada.xin@nio.com></at>', 'NT2ADD-5002 <at email=longyue.wang@nio.com></at>']
    loc = '/media/nio/codes/shiting/nfs51/display_data/nt2_cn_eval_data/hardcase/'
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
                            "content": f"**⏰ 提醒时间：**\n{datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')}\n**🗒 文件存储地址：**\n{loc}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**👤 已解析文件：**\n{jira_list}".format(jira_list='\n'.join(jira_list)),
                            "tag": "lark_md"
                        }
                    }
                ],
                "tag": "div"
            }
        ],
        "header": {
            "title": {
                "content": "文件解析完成（发送测试） 🎉",
                "tag": "plain_text"
            }
        }
    }
    FM = FeishuMessage()
    # res = FM.get_chat_id()
    FM.batch_message({'open_ids': ['ou_107a29071bdefbbf34181922353e9e01', 'ou_b3d4ba59f76ccaacabd080b850238a66']}, 'interactive', interactive)
    FM.message({'type': 'chat_id', 'id': 'oc_4161dee2f30c713a9cc35aa4e5222650'},
               'interactive',
               interactive)


if __name__ == '__main__':
    main()
