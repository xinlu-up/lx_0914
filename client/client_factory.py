from api.work_item_info import WorkItemInfo
from api.project_view import ProjectView
from api.work_item_configuration import WorkItemConfiguration
from api.work_item_list import WorkItemList



class LarkClientFactory:
    def __init__(self, lark_client):
        self.lark_client = lark_client

    def create_project_view(self):
        return ProjectView(self.lark_client)

    def create_work_item_info(self):
        return WorkItemInfo(self.lark_client)

    def create_work_item_configuration(self):
        return WorkItemConfiguration(self.lark_client)

    def create_work_item_list(self):
        return WorkItemList(self.lark_client)
