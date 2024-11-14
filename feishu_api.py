# -*- encoding: utf-8 -*-
"""
飞书 API
"""
import json
import numpy
import logging
import requests


class FeishuAPI:

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

        self.feishu_host = 'https://open.feishu.cn'
        self.url_tenant_access_token = '/open-apis/auth/v3/tenant_access_token/internal'
        self.url_group_message = '/open-apis/im/v1/messages?receive_id_type=chat_id'
        self.url_get_id = '/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id'
        self.url_bitable_apps = '/open-apis/bitable/v1/apps'
        self.url_upload_file = '/open-apis/drive/v1/medias/upload_all'
        self.url_import = '/open-apis/drive/v1/import_tasks'
        self.url_export = '/open-apis/drive/v1/export_tasks'

        self.headers_json = {"Content-Type": "application/json; charset=utf-8"}
        self.tenant_access_token = self.get_app_access_token()
        self.headers_access = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.tenant_access_token}"
        }

    def get_app_access_token(self):
        """
        获取 app_access_token
        :return:
        """
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        res = requests.post(
            url=self.feishu_host + self.url_tenant_access_token, data=json.dumps(data), headers=self.headers_json)

        logging.error(res.text)
        return json.loads(res.text)['tenant_access_token']


class FeishuUserApi(FeishuAPI):
    """
    用户
    """

    def get_user_id(self, username):
        name_list = username.split(',')
        email_list = list(map(lambda s: s + '@nio.com', name_list))
        req = {
            "emails": email_list,
            "mobiles": []
        }
        resp = requests.post(url=self.feishu_host + self.url_get_id, headers=self.headers_access, json=req)
        return resp.text


class FeishuBiTable(FeishuAPI):
    """
    多维表格
    """

    def create_bitable_table(self, file_name, folder_token='fldcn6jxj7vwMWlai6YquYUgWrd'):
        """
        创建多维表格, 使用之前请确保机器人有当前目录权限,
        可将机器人拉到群里，将文件夹分享到群
        :param file_name: 多维表格名称
        :param folder_token: folder_token, 不填使用默认值
        :return: file_url: 飞书文档链接
        """
        data = {"name": file_name, "folder_token": folder_token}
        res = requests.post(url=self.feishu_host + self.url_bitable_apps,
                            data=json.dumps(data), headers=self.headers_access)
        res_text = json.loads(res.text)
        file_url = res_text['data']['app']['url']
        app_token = res_text['data']['app']['app_token']
        app_folder_token = res_text['data']['app']['folder_token']
        return app_token, app_folder_token, file_url

    def create_bitable_table_data_sheet(self, app_token, table_name):
        """
        创建数据表
        :param app_token:
        :param table_name: 数据表名称
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables'
        data = {"table": {"name": table_name}}
        requests.post(url=url, headers=self.headers_access, data=json.dumps(data))

    def update_bitable_table_data_sheet_name(self, app_token, table_id, table_name):
        """
        更新数据表名称
        :param app_token:
        :param table_id: 数据表ID
        :param table_name: 新名称
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id
        data = {"name": table_name}
        requests.patch(url=url, headers=self.headers_access, data=json.dumps(data))

    def del_bitable_table_data_sheet(self, app_token, table_id):
        """
        删除数据表
        :param app_token:
        :param table_id: 数据表ID
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id
        requests.delete(url=url, headers=self.headers_access)

    def get_bitable_table_data_sheet(self, app_token):
        """
        获取所有的数据表
        :param app_token:
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables'
        res = requests.get(url=url, headers=self.headers_access)
        res_text = json.loads(res.text)
        tables = res_text['data']['items']
        return tables

    def get_bitable_table_views(self, app_token, table_id):
        """
        获取对应数据表所有视图
        :param app_token:
        :param table_id: 数据表ID
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id + '/views'
        res = requests.get(url=url, headers=self.headers_access)
        res_text = json.loads(res.text)
        return res_text['data']['items']

    def update_bitable_table_view_name(self, app_token, table_id, view_id, view_name):
        """
        更新数据表对应视图名称
        :param app_token:
        :param table_id: 数据表ID
        :param view_id: 视图ID
        :param view_name: 新名称
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/views/{view_id}"
        data = {"view_name": view_name}
        requests.patch(url=url, headers=self.headers_access, data=json.dumps(data))

    def update_bitable_table_view(self, app_token, table_id, view_id, update_data):
        """
        更新数据表对应视图名称
        :param app_token:
        :param table_id: 数据表ID
        :param view_id: 视图ID
        :param update_data: 更新内容
        :return:
        """
        print(json.dumps(update_data))
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/views/{view_id}"
        res = requests.patch(url=url, headers=self.headers_access, data=json.dumps(update_data)).json()
        print(res)

    def create_bitabl_table_views(self, app_token, table_id, view_name, view_type='grid'):
        """
        新增视图
        :param app_token:
        :param table_id: 数据表ID
        :param view_type: 视图类型, 默认 grid
        :param view_name: 视图名称
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id + '/views'
        view_data = {"view_name": view_name, "view_type": view_type}
        res = requests.post(url=url, headers=self.headers_access, data=json.dumps(view_data)).json()
        return res['data']['view']['view_id']

    def update_bitabl_table_field_name(self, app_token, table_id, field_name, new_field):
        """
        更新数据表字段
        参考飞书文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-field/guide
        :param app_token:
        :param table_id: 数据表ID
        :param field_name: 字段名称
        :param new_field: 字段,例 {"field_name": "字段名称", "type": "字段类型"}
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id + '/fields'
        res = requests.get(url=url, headers=self.headers_access)
        for field in json.loads(res.text)['data']['items']:
            _field_name = field['field_name']
            if _field_name == field_name:
                get_url = url + '/' + field['field_id']
                res = requests.put(url=get_url, headers=self.headers_access, data=json.dumps(new_field))
                logging.error(f'{res.text}, {field_name}')

    def delete_bitabl_table_field_name(self, app_token, table_id, field_name):
        """
        删除数据表字段
        参考飞书文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-field/guide
        :param app_token:
        :param table_id: 数据表ID
        :param field_name: 字段名称
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id + '/fields'
        res = requests.get(url=url, headers=self.headers_access)
        for field in json.loads(res.text)['data']['items']:
            _field_name = field['field_name']
            if _field_name == field_name:
                get_url = url + '/' + field['field_id']
                res = requests.delete(url=get_url, headers=self.headers_access)
                logging.error(f'{res.text}, {field_name}')

    def create_bitabl_table_field(self, app_token, table_id, field_list):
        """
        新增数据表格字段
        例子: [
            {"field_name": "名称", "type": 1},
            {"field_name": "下拉选择", "type": 3, "property": {"options": [{"name": "选项1"},{"name": "选项2"}]}}
        ]
        格式参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-field/create
        :param app_token:
        :param table_id: 数据表ID
        :param field_list: field_list
        :return:
        """
        url = self.feishu_host + self.url_bitable_apps + '/' + app_token + '/tables' + '/' + table_id + '/fields'

        for field in field_list:
            res = requests.post(url=url, headers=self.headers_access, data=json.dumps(field))
            logging.error(res.text)

    def get_bitabl_tables_fields(self, app_token, table_id, view_id=""):
        """
        获取字段列表
        :param app_token:
        :param table_id: 数据表ID
        :param view_id: 视图ID
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/fields?view_id={view_id}"
        res = requests.get(url, headers=self.headers_access).json()
        if 'items' in res['data']:
            return res['data']['items']
        return []

    def create_bitabl_tables_records(self, app_token, table_id, records, field=None):
        """
        新增数据表记录,返回指定字段 数据list参考：
        [
            {
                "fields": {
                    "名称": "测试1",
                    "下拉选择": "选项1"}
            },
            {
                "fields": {
                    "名称": "测试2",
                    "下拉选择": "选项2"}
            }
        ]
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create
        :param app_token:
        :param table_id: 数据表ID
        :param records: 数据list
        :param field
        :return:
        """

        if len(records) > 500:
            page_count = int(len(records) / 500) + 1
        else:
            page_count = 1

        array = numpy.array(records)
        new_array = numpy.array_split(array, page_count)
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records/batch_create"

        record_ids = []
        for record in new_array:
            record_data = {"records": list(record)}
            res = requests.post(url=url, headers=self.headers_access, json=record_data)
            res_text = res.json()
            if res_text['code'] != 0:
                logging.error(res.text)
                return None
            else:
                if 'data' in res_text and 'records' in res_text['data']:
                    data = res_text['data']['records']
                    if field is None:
                        for i in data:
                            record_ids.append(i['record_id'])
                    else:
                        for i in data:
                            field_val = i['fields'][field]
                            record_id = i['record_id']
                            record_ids.append({"id": field_val, "record_id": record_id})
        return record_ids

    def update_bitabl_members(self, app_token, member_type='email', email='yanping.zhou1.o@nio.com'):
        """
        转移多维表格给指定用户
        :param app_token:
        :param member_type:
        :param email:
        :return:
        """
        url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{app_token}/members/transfer_owner?type=bitable"

        data = {
            "member_type": member_type,
            "member_id": email
        }
        res = requests.post(url, headers=self.headers_access, data=json.dumps(data))
        logging.error(res.text)

    def get_bitabl_records(self, app_token, table_id, view_id):
        """
        获取多维表格记录
        :param app_token:
        :param table_id:
        :param view_id
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records?"
        args = f'view_id={view_id}&page_size=500'
        res_list = []

        res = requests.get(url + args, headers=self.headers_access)
        res_text = res.json()

        if 'page_token' in res_text['data']:
            page_token = res_text['data']['page_token']

            for i in res_text['data']['items']:
                res_list.append(i)

            while page_token:
                args = f'view_id={view_id}&page_size=500&page_token={page_token}'
                res = requests.get(url + args, headers=self.headers_access)
                res_text = res.json()
                page_token = res_text['data']['page_token']
                if page_token == '':
                    page_token = False

                if res_text['data']['items'] is None:
                    page_token = False
                else:
                    for i in res_text['data']['items']:
                        res_list.append(i)

        return res_list

    def get_bitabl_record_list(self, app_token, table_id, filter_str, sort='["创建时间 DESC"]'):
        """
        使用 filter 查询多维表格记录
        :param app_token:
        :param table_id:
        :param filter_str
        :param sort
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records?" \
              f"text_field_as_array=false&filter={filter_str}&sort={sort}"
        args = f'&page_size=500'
        print(url + args)
        res = requests.get(url + args, headers=self.headers_access)         # 这个地方失败了
        res_text = res.json()

        record_id = None
        res_list = []
        if 'data' in res_text:

            if res_text['data']['items'] is None:
                return None

            for i in res_text['data']['items']:
                res_list.append(i)

            if 'page_token' in res_text['data']:
                page_token = res_text['data']['page_token']

                while page_token:
                    args = f'&page_size=500&page_token={page_token}'
                    res = requests.get(url + args, headers=self.headers_access)
                    res_text = res.json()
                    if 'data' in res_text:
                        if 'page_token' in res_text['data']:
                            page_token = res_text['data']['page_token']
                            if page_token == '':
                                page_token = False
                        else:
                            page_token = False

                        if res_text['data']['items'] is None:
                            page_token = False
                        else:
                            for i in res_text['data']['items']:
                                res_list.append(i)
                    else:
                        print(res_text)
        else:
            print(res_text)

        if len(res_list) > 0:
            record_id = res_list
        return record_id

    def get_bitabl_record_by_record_id(self, app_token, table_id, record_id, text_field_as_array=False):
        """
        使用 record_id 查询多维表格记录
        :param app_token:
        :param table_id:
        :param record_id
        :param text_field_as_array
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records/{record_id}"
        if text_field_as_array:
            url += '?text_field_as_array=true'
        res = requests.get(url, headers=self.headers_access)
        res_text = res.json()

        if 'data' in res_text:
            return res_text['data']

        return None

    def update_bitabl_records_one(self, app_token, table_id, record_id, fields):
        """
        更新单条多维表格记录
        :param app_token:
        :param table_id:
        :param record_id
        :param fields
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records/{record_id}"
        res = requests.put(url, headers=self.headers_access, data=json.dumps(fields))
        print(res.text)

    def update_bitabl_tables_records(self, app_token, table_id, records):
        """
        更新数据表记录, 数据list参考：
        [
            {   "record_id": "",
                "fields": {
                    "名称": "测试1",
                    "下拉选择": "选项1"}
            },
            {
                "record_id": "",
                "fields": {
                    "名称": "测试2",
                    "下拉选择": "选项2"}
            }
        ]
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create
        :param app_token:
        :param table_id: 数据表ID
        :param records: 数据list
        :return:
        """

        if len(records) > 500:
            page_count = int(len(records) / 500) + 1
        else:
            page_count = 1

        array = numpy.array(records)
        new_array = numpy.array_split(array, page_count)
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records/batch_update"
        for record in new_array:
            if len(record) > 0:
                record_data = {"records": list(record)}
                res = requests.post(url=url, headers=self.headers_access, data=json.dumps(record_data))
                res_text = res.json()
                if res_text['code'] != 0:
                    logging.error(res.text)

    def delete_record_list(self, app_token, table_id, record_id_list):
        """
        删除多维表格记录
        :param app_token:
        :param table_id:
        :param record_id_list:
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records/batch_delete"
        record_data = {"records": record_id_list}
        res = requests.post(url=url, headers=self.headers_access, data=json.dumps(record_data))
        logging.error(res.text)

    def download_files(self, file_token):
        return requests.get(url=file_token, headers=self.headers_access)

    def get_bitabl_record_list_text_field_as_array(self, app_token, table_id, filter_str):
        """
        使用 filter 查询多维表格记录
        :param app_token:
        :param table_id:
        :param filter_str
        :return:
        """
        url = f"{self.feishu_host}{self.url_bitable_apps}/{app_token}/tables/{table_id}/records?" \
              f"text_field_as_array=true&filter={filter_str}"
        args = f'&page_size=500'

        res = requests.get(url + args, headers=self.headers_access)
        res_text = res.json()
        record_id = None
        res_list = []

        if res_text['data']['items'] is None:
            return None

        for i in res_text['data']['items']:
            res_list.append(i)

        if 'page_token' in res_text['data']:
            page_token = res_text['data']['page_token']

            while page_token:
                args = f'&page_size=500&page_token={page_token}'
                res = requests.get(url + args, headers=self.headers_access)
                res_text = res.json()
                page_token = res_text['data']['page_token']
                if page_token == '':
                    page_token = False

                if res_text['data']['items'] is None:
                    page_token = False
                else:
                    for i in res_text['data']['items']:
                        res_list.append(i)

        if len(res_list) > 0:
            record_id = res_list
        return record_id
