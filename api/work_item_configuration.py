from api.refresh_token import AutoRefreshMeta


class WorkItemConfiguration(metaclass=AutoRefreshMeta):
    def __init__(self, lark_client):
        self._lark_client = lark_client
        self.filed_path = f"/{self._lark_client.project_key}/field"

    # def update_custom_fields(self):
    #     params = {
    #         "field_key": "field_f7cb6c",
    #         "help_description": "openapi_update_help_description",
    #         "authorized_roles": ["_master"],
    #         "default_value": ["c7uqvx5j1"],
    #         "field_value": [{
    #             "label": "kkkkk",
    #             "action": 0
    #         }
    #         ]
    #     }
    #     path = f"/{self.filed_path}/{self._lark_client.work_item_type_key}"
    #     resp = self._lark_client.send_request("put", path, data=params)
    #     return resp.json()
