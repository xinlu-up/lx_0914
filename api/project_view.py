from api.refresh_token import AutoRefreshMeta
class ProjectView(metaclass=AutoRefreshMeta):
    def __init__(self, lark_client):
        self._lark_client = lark_client

    def get_view_work_item_id_list(self, view_id: str, page_size: int = 200, page_num: int = 1):
        """
        获取视图下的工作项列表
        :param project_key: 项目id，或者项目域名
        :param view_id: 视图ID
        :param page_size: 每页数据，最大200
        :param page_num: 分页页码，从1开始，默认为1
        :return:
        """
        path = f"/{self._lark_client.project_key}/fix_view/{view_id}"
        data = {
            "page_size": page_size,
            "page_num": page_num
        }
        resp = self._lark_client.send_request("get", path, data=data)
        return resp.json()
