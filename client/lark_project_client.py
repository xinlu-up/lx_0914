import requests
import configs as configs
from client.http_client import HttpClient
from client.client_factory import LarkClientFactory
import logging

class LarkClientSingleton:
    _instances = {}

    def __new__(cls, project_key):
        if project_key not in cls._instances:                   # project_key == 'sj_test'
            cls._instances[project_key] = super().__new__(cls)
            cls._instances[project_key].project_key = project_key
            cls._instances[project_key]._lark_client = cls._create_lark_client(project_key)
        return cls._instances[project_key]._lark_client

    @staticmethod
    def _create_lark_client(project_key):
        user_key = configs.USER_KEY
        plugin_id = configs.PLUGIN_ID
        plugin_secret = configs.PLUGIN_SECRET
        return LarkProjectClient(user_key, plugin_id, plugin_secret, project_key)


class LarkProjectClient(HttpClient):
    def __init__(self, user_key: str, plugin_id: str, plugin_secret: str, project_key: str, max_retries=2,
                 retry_delay=1):
        super().__init__(max_retries, retry_delay, configs.API_HOST)
        self.user_key = user_key           # USER_KEY = "7324792892365586435"
        self.project_key = project_key      # sj_test
        self.plugin_data = {
            "plugin_id": plugin_id,
            "plugin_secret": plugin_secret,
            "type": 0  # 0为plugin_token，1为虚拟plugin_token，虚拟token权限临时生效，不受插件发版限制
        }
        self.refresh_authorization()
        self.factory = LarkClientFactory(self)
        self.work_item_type_key = None      # story

    def get_token(self) -> str:
        url = f"{self.api_host}/authen/plugin_token"          # 'https://project.feishu.cn/open_api/authen/plugin_token'
        response = requests.post(url, headers=self.headers, json=self.plugin_data)
        response.raise_for_status()
        print(response.json()["data"]["token"])         # p-f245cf6e-25c5-4d74-8561-d809b1bff690
        return response.json()["data"]["token"]            # 返回了token

    def refresh_authorization(self):
        self.headers.update({'X-USER-KEY': self.user_key})
        self.headers.update({'X-PLUGIN-TOKEN': self.get_token()})

    def get_work_type(self, name):
        path = f"/{self.project_key}/work_item/all-types"            # '/sj_test/work_item/all-types'
        resp = self.send_request("get", path)           # 返回时空的 path = '/sj_test/work_item/all-types'
        if resp is not None and resp.status_code == 200:
            print(type(resp))                # <class 'requests.models.Response'>
            resp = resp.json()
            
            if 'data' in resp:
                print(resp['data'])
                if 'name' in resp['data']:
                    print(item['type_key'])
                    
                    
            for item in resp['data']:
                print(item)
                if item['name'] == name:        # ‘name' = '需求‘
                    return item['type_key']     # return story
        return None

    def use_work_type(self, work_type):                             # 第二个主函数调用的是这个函数   work_type = ‘story'              
        work_item_type_key = self.get_work_type(work_type)       # 这个地方返回时空的
        if work_item_type_key is not None:
            self.work_item_type_key = self.get_work_type(work_type)
        else:
            logging.error("work_item_type_key is None")
        return None

    def work_item_info(self):
        return self.factory.create_work_item_info()

    def project_view(self):
        return self.factory.create_project_view()

    def work_item_configuration(self):
        return self.factory.create_work_item_configuration()

    def work_item_list(self):
        return self.factory.create_work_item_list()