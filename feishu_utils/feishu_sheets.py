#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Feishu Sheets Client"""
import json
import os
import requests


class FeishuSheets:
    _FEISHU_HOST = 'https://open.feishu.cn/open-apis'

    def __init__(self):
        token_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config',
                                  'parking_test_token.json')
        if not os.path.exists(token_file):
            print('FeishuSheets init failed and parking_test_token.json not exist')
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
            'Authorization': 'Bearer {}'.format(self._access_token),
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

    def get_sheets_metainfo(self, spreadsheet_id):
        """get spreadsheet meta information"""
        url = '{}/sheets/v2/spreadsheets/{}/metainfo'.format(self._FEISHU_HOST, spreadsheet_id)
        res = requests.get(url, headers=self._headers)
        if res.status_code == 200:
            return res.json()
        return None

    def get_sheets_list(self, spreadsheet_id):
        """get all the sheets meta data of one spreadsheet"""
        res = self.get_sheets_metainfo(spreadsheet_id)
        sheets_list = dict()
        if res and res.get('data') and res['data'].get('sheets'):
            for item in res['data'].get('sheets', []):
                sheets_list[item.get('title')] = item.get('sheetId')
            return sheets_list
        return None

    def get_multi_range_sheet_content(self, spreadsheet_id, search_range):
        """get multiple search range sheet content, e.g.ranges=Q7PlXT!A2:B6,0b6377!B1:C8"""
        url = '{}/sheets/v2/spreadsheets/{}/values_batch_get?ranges={}'.format(self._FEISHU_HOST, spreadsheet_id,
                                                                               search_range)
        res = requests.get(url, headers=self._headers)
        if res.status_code == 200:
            content = list()
            for range_data in res.json().get('data', {}).get('valueRanges', {}):
                content.append(range_data.get('values'))
            return content
        return None

    def get_sheet_content(self, spreadsheet_id, sheet_title=None, sheet_range=None):
        """get sheet content by sheet title and range"""
        sheets_list = self.get_sheets_list(spreadsheet_id)
        if not sheets_list or (sheet_title and sheet_title not in sheets_list):
            return None
        if sheet_title:
            sheet_id = sheets_list.get(sheet_title)
        else:
            sheet_id = list(sheets_list.values())[0]
        if sheet_range:
            search_range = '{}!{}'.format(sheet_id, sheet_range)
        else:
            search_range = sheet_id
        url = '{}/sheets/v2/spreadsheets/{}/values/{}'.format(self._FEISHU_HOST, spreadsheet_id, search_range)
        res = requests.get(url, headers=self._headers)
        if res.status_code == 200:
            return res.json().get('data', {}).get('valueRange', {}).get('values')
        return None

    def update_sheets_content(self, spreadsheet_id, values, sheet_title=None, sheet_range=None):
        """update content into spreadsheet"""
        sheets_list = self.get_sheets_list(spreadsheet_id)
        if not sheets_list or (sheet_title and sheet_title not in sheets_list):
            return None
        if sheet_title:
            sheet_id = sheets_list.get(sheet_title)
        else:
            sheet_id = list(sheets_list.values())[0]
        if sheet_range:
            update_range = '{}!{}'.format(sheet_id, sheet_range)
        else:
            update_range = sheet_id
        print(update_range)
        url = '{}/sheets/v2/spreadsheets/{}/values'.format(self._FEISHU_HOST, spreadsheet_id)
        body = {
            "valueRange": {
                "range": update_range,
                "values": values
            }
        }
        res = requests.put(url, json.dumps(body), headers=self._headers)
        print(res.json())
        if res.status_code == 200 and res.json().get('code') == 0:
            return True
        return False

    def add_to_content(self,spreadsheet_id, values, sheet_title=None, sheet_range=None):
        sheets_list = self.get_sheets_list(spreadsheet_id)
        if not sheets_list or (sheet_title and sheet_title not in sheets_list):
            return None
        if sheet_title:
            sheet_id = sheets_list.get(sheet_title)
        else:
            sheet_id = list(sheets_list.values())[0]
        if sheet_range:
            update_range = '{}!{}'.format(sheet_id, sheet_range)
        else:
            update_range = sheet_id
        print(update_range)
        url = '{}/sheets/v2/spreadsheets/{}/values_append'.format(self._FEISHU_HOST,spreadsheet_id)
        body = {
            "valueRange": {
                "range": update_range,
                "values": values
            }
        }
        res = requests.post(url, json.dumps(body), headers=self._headers)
        print(res.json())
        if res.status_code == 200 and res.json().get('code') == 0:
            return True
        return False

    def create_new_spreadsheets(self, title):
        """create a new spreadsheet document"""
        url = '{}/sheets/v3/spreadsheets'.format(self._FEISHU_HOST)
        body = {
            'title': title,
        }
        res = requests.post(url, json.dumps(body), headers=self._headers)
        if res.status_code == 200:
            res = res.json()
            print(res)
            return res.get('data')
        return None

    def add_new_column_row(self, spreadsheet_id, sheet_name, start_index, end_index, insert_type='COLUMNS',
                           inherit_style='BEFORE'):
        """add new column in spreadsheet document"""
        sheets_list = self.get_sheets_list(spreadsheet_id)
        if not sheets_list or (sheet_name and sheet_name not in sheets_list):
            return False
        if sheet_name:
            sheet_id = sheets_list.get(sheet_name)
        else:
            sheet_id = list(sheets_list.values())[0]
        url = '{}/sheets/v2/spreadsheets/{}/insert_dimension_range'.format(self._FEISHU_HOST, spreadsheet_id)
        body = {
            "dimension":
                {
                    "sheetId": sheet_id,
                    "majorDimension": insert_type,
                    "startIndex": start_index,
                    "endIndex": end_index
                },
            "inheritStyle": inherit_style
        }
        res = requests.post(url, json.dumps(body), headers=self._headers)
        if res.status_code == 200 and res.json().get('code') == 0:
            return True
        return False

    def add_new_sheet(self, spreadsheet_id, sheet_name):
        """add a new sheet in one existed spreadsheet"""
        url = '{}/sheets/v2/spreadsheets/{}/sheets_batch_update'.format(self._FEISHU_HOST, spreadsheet_id)
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": sheet_name,
                            "index": 1
                        }
                    }
                }
            ]
        }
        res = requests.post(url, json.dumps(body), headers=self._headers)
        if res.status_code == 200 and res.json().get('code') == 0:
            return True
        return False

    def add_edit_sheet_permission(self, spreadsheet_id, email):
        """add edit permission by user email"""
        open_id = self.get_open_id_by_email(email)
        if not open_id:
            return False
        url = '{}/drive/permission/member/create'.format(self._FEISHU_HOST)
        body = {
            "token": spreadsheet_id,
            "type": "sheet",
            "members": [
                {
                    "member_type": "openid",
                    "member_id": open_id,
                    "perm": "edit"
                }
            ]
        }
        res = requests.post(url, json.dumps(body), headers=self._headers)
        if res.status_code == 200 and res.json().get('code') == 0:
            return True
        return False

    def get_open_id_by_email(self, email):
        """get open_id by user email"""
        url = '{}/user/v1/batch_get_id?emails={}'.format(self._FEISHU_HOST, email)
        res = requests.get(url, headers=self._headers)
        if res.status_code == 200 and res.json().get('code') == 0:
            return res.json().get('data').get('email_users').get(email)[0].get('open_id')
        return None

    def get_raw_content(self, doctoken):
        url = '{}/doc/v2/{}/raw_content'.format(self._FEISHU_HOST, doctoken)
        res = requests.get(url, headers=self._headers)
        if res.status_code == 200 and res.json().get('code') == 0:
            return res.json().get('data')
        return None

def main():
    spreadsheet_id = '' #'需要改成自己创建的sheet id'
    sheet_client = FeishuSheets()
    res = sheet_client.get_raw_content('doccnhhpcQnwaSOQmrKCyjyh3ph')
    jiras = res.get('content').split('\n')[1:]
    for jira in jiras:
        if jira == '':
            continue
        jira = jira.split(' ')[0]
        jira = jira.split('/')[-1]
    print(sheet_client.add_new_sheet(spreadsheet_id, 'test'))
    open_id = sheet_client.get_open_id_by_email('')#'需要增加nio邮箱'
    print(open_id)
    # print(sheet_client.create_new_spreadsheets('NT2.0 CN评测数据统计test'))
    print(sheet_client.add_edit_sheet_permission(spreadsheet_id, 'xxxx'))#'需要增加nio邮箱'
    print(sheet_client.get_sheet_content(spreadsheet_id, 'NT 2.0评测数据集标签', 'A1:Z2'))


if __name__ == '__main__':
    main()
