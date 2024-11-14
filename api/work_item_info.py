from api.refresh_token import AutoRefreshMeta


class WorkItemInfo(metaclass=AutoRefreshMeta):

    def __init__(self, lark_client):
        self._lark_client = lark_client
        self.path = f"/{self._lark_client.project_key}/work_item/{self._lark_client.work_item_type_key}"
        # path = https://project.feishu.cn/open_api/sj_test/work_item/story
    
    def get_assign_workitem(self,size):
        """
        获取指定的工作项列表（非跨空间）
        size:代表访问的数据量
    
        """
        # path = f"/{self.path}//workflow/query"
        path = f'/sj_test/work_item/filter'       # 这个地方我写死了 
        param = {
            "work_item_type_keys": [
                "story"
            ],
            "page_size":size
        }
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()

    def create_work_items(self, name, template_id, field_value_pairs=[]):
        """
        创建工作项
        :param name: 工作项名称
        :param work_item_type_key:工作项类型
        :param update_fields:模板ID
        :param update_fields:创建工作项的具体字段
        :return:
        """
        param = {
            "name": name,
            "template_id": template_id,
            "work_item_type_key": self._lark_client.work_item_type_key,
            "field_value_pairs": field_value_pairs
        }
        path = f"/{self._lark_client.project_key}/work_item/create"
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()

    def update_work_items_by_id(self, work_item_id, update_fields):       # 调用的是这个函数
        """
        更新工作项
        :param work_item_id: 工作项ID
        :param update_fields: 要更新的字段列表 list<FieldValuePair> 例：[{"field_key": "field_7c8399", "field_value": 1700706827000}]
        :return:
        """
        param = {"update_fields": update_fields}
        path = f"/{self.path}/{work_item_id}"      # path后面加入工作项id
        resp = self._lark_client.send_request("put", path, data=param)
        return resp.json()

    def delete_work_items_by_id(self, work_item_id):
        """
        删除工作项
        :param work_item_id: 工作项ID
        :return:
        """
        path = f"/{self.path}/{work_item_id}"        # story/4423432073
        resp = self._lark_client.send_request("delete", path)
        return resp.json()

    def abort_work_items_by_id(self, work_item_id, is_aborted: bool, reason: str):
        """
        更新工作项
        :param work_item_id: 工作项ID
        :param is_aborted: 终止或恢复需求，true为终止，false为恢复
        :param reason: 终止或恢复需求的原因
        :return:
        """
        param = {
            "is_aborted": is_aborted,
            "reason": reason
        }
        path = f"/{self.path}/{work_item_id}/abort"
        resp = self._lark_client.send_request("put", path, data=param)
        return resp.json()

    def query_work_items_by_ids(self, work_item_ids, fields=None, expand=None):
        """
        获取工作项详情
        :param work_item_ids: 工作项ID列表，一次请求最大50个
        :param fields: 定义需要返回的字段，非必填，默认返回全部
        :param expand: 额外参数：
            need_workflow:是否需要工作流信息（目前只支持节点流）
            need_multi_text:是否需要富文本详细信息
            relation_fields_detail：是否需要关联字段详细信息
        :return:
        """
        expand  = {
            'need_workflow':True,
            'need_multi_text':True,
            'relation_fields_detail':True
        }
        path = f"/{self.path}/query"
        data = {"work_item_ids": work_item_ids, "fields": fields, "expand": expand}
        print(path)
        resp = self._lark_client.send_request("post", path, data=data)
        return resp.json()


        
    
    # def get_field_by_id(self,work_item_id):
    #     """
    #     1. 通过工作项id获取指定字段
    #     """
    #     path = f"/{self.path}/query" 
    #     data = {"work_item_ids": work_item_id}
    #     resp = self._lark_client.send_request("post", path,data = data)
    #     return resp.json()
        

    def get_work_items_meta(self):
        """
        获取创建工作项元数据
        :return:
        """
        path = f"/{self.path}/meta"
        resp = self._lark_client.send_request("get", path)
        return resp.json()

    def get_workflow_query(self, work_item_id, flow_type=0, fields=None):
        """
        获取工作流详情
        :param work_item_id: 工作项ID
        :param flow_type: 工作流类型
        :param fields: 定义需要返回的字段，非必填，默认返回全部
        工作流类型：
        0：节点流，节点流工作项举例：需求等
        1 ：状态流，状态流工作项举例：缺陷、版本等
        非必填，默认为0（节点流）
        :return:
        """
        path = f"/{self.path}/{work_item_id}/workflow/query"
        param = {
            "flow_type": flow_type,
            "fields": fields
        }
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()

    def update_work_item_node_by_id(self, work_item_id, node_id, node_owners=[], node_schedule=None,
                                    schedules=[], fields=[], role_assignees=[]):
        """
        节点完成、回滚
        :param work_item_id: 工作项ID
        :param node_id: 节点id
        :param action: 操作类型，可选值为confirm(完成),rollback(回滚) 例：{"action": "confirm"}
        :param rollback_reason: 回滚原因，当action为rollback时必填
        :return:
        """
        path = f"/{self.path}/{work_item_id}/node/{node_id}"
        param = {
            "node_owners": node_owners,
            "node_schedule": node_schedule,
            "schedules": schedules,
            "fields": fields,
            "role_assignees": role_assignees
        }
        resp = self._lark_client.send_request("put", path, data=param)
        return resp.json()

    def operate_work_item_node_by_id(self, work_item_id, node_id, action, rollback_reason="", node_owners=[],
                                     node_schedule=None, schedules=[], fields=[], role_assignees=[]):
        """
        节点完成、回滚
        :param work_item_id: 工作项ID
        :param node_id: 节点id
        :param action: 操作类型，可选值为confirm(完成),rollback(回滚) 例：{"action": "confirm"}
        :param rollback_reason: 回滚原因，当action为rollback时必填
        :return:
        """
        path = f"/{self.path}/{work_item_id}/node/{node_id}/operate"
        param = {
            "action": action,
            "rollback_reason": rollback_reason,
            "node_owners": node_owners,
            "node_schedule": node_schedule,
            "schedules": schedules,
            "fields": fields,
            "role_assignees": role_assignees
        }
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()

    def change_workflow_state_by_id(self, work_item_id, transition_id, role_owners=[], fields=[]):
        """
        状态流转
        :param work_item_id: 工作项ID
        :param transition_id: 节点id 流转到下一状态的id，从获取工作流详情接口查询状态流获取
        :return:
        """
        path = f"/{self.path}/{work_item_id}/node/state_change"
        param = {
            "transition_id": transition_id,
            "role_owners": role_owners,
            "fields": fields
        }
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()
