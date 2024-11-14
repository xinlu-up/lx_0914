from api.refresh_token import AutoRefreshMeta


class WorkItemList(metaclass=AutoRefreshMeta):

    def __init__(self, lark_client):
        self._lark_client = lark_client

    def get_work_item_list_single_space(self, start_time, end_time, page_size=200, page_num=1):
        path = f"/{self._lark_client.project_key}/work_item/filter"
        param = {
            "work_item_type_keys": [
                self._lark_client.work_item_type_key
            ],
            "created_at": {
                "start": start_time,
                "end": end_time
            },
            "page_size": page_size,
            "page_num": page_num
        }
        resp = self._lark_client.send_request("post", path, data=param)
        return resp.json()
