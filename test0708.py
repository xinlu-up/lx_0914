from client.lark_project_client import LarkClientSingleton
# from api.work_item_info import update_work_items_by_id
import json
import logging
import time
from feishu_utils.feishu_message import FeishuMessage
from feishu_utils.feishu_sheets import FeishuSheets
import requests
from feishu_api import *
import schedule



def get_fields(res:json):
    # print(type(res['data']))    # 这应该是个列表  list
    # print(len(res['data']))    # 1
    for item in res['data']:             # 这个item是每一个需求
        # print(type(item))      # dict
        for it in item:
            if it == 'name':
                name = item[it]
                print("需求名称：",name)
                
            if it == 'created_at':
                created_time = item[it]
                print(type(created_time))       # int 
                print(created_time)
                
            if it == 'fields':
                for i in item['fields']:      # string
                    # print(i['field_key'])
                    # print(i)
                    if i['field_key'] == 'field_d97763':
                        bundle_uuid = i['field_value']
                        print(type(bundle_uuid))
                        isdight = bundle_uuid.isdigit()
                        print("bundle_uuid：",bundle_uuid)
                        # print(isdight)
                        if isdight:
                            print("bundle_uuid是纯数字")
                        else:
                            print("bundle_uuid不是纯数字")
                            ############### 这个地方要进入提醒： 向对应平台的管理员发送报警信息；这个地方只要检测一遍；#################

                    if i['field_key'] == 'field_0a903a':
                        version = i['field_value'][0]['label']    # 这个0要不要删除？
                        print("版本模式：",version)

                    if i['field_key'] == 'priority':
                        priority = i['field_value']['label']
                        print("优先级：",priority)
                    
                    if i['field_key'] == 'field_c7a8e8':
                        base_version = i['field_value']
                        
                        print("基准版本：",base_version)
                        if base_version.isdigit():
                            print("base_version是纯数字")
                        else:
                            print("base_version不是纯数字")
                            ############### 这个地方要进入提醒： 向对应平台的管理员发送报警信息；这个地方只要检测一遍；#################
                        
                    if i['field_key'] == 'field_bf1d36':
                        func = i['field_value'][0]['label']
                        print("执行功能：",func)
                    
                    if i['field_key'] == 'field_a50b6d':
                        stage_set = i['field_value']['label']
                        if stage_set == '默认全量场景集':
                            print(stage_set)
                        else:
                            print("不是默认场景集")
                            ############### 这个地方要进入提醒： 向对应平台的管理员发送报警信息；这个地方只要检测一遍；#################

    
def get_all_id(res2):
    """ 
    :type res2:json
    :rtype :List
    """
    id_list = []
    for items in res2['data']:
        for item in items:
            if item == 'id':
                id = items[item]
                id_list.append(id)
    
    if len(id_list) == 0:
        logging.info("faild to get ids")
    logging.info("id的长度为：{}".format(len(id_list)))
    
    print(id_list)
    return id_list
                
def get_week_id(res2):
    """
     :type res2:json
    :rtype :List
    """
    timestamp = time.time()
    now_timestamp = int(timestamp*1000)
    seven_days_ago = now_timestamp - 7 * 86400000 
    print(now_timestamp)
    print(seven_days_ago)
    # seven_days_ago = 1719504000000
    
    
    week_id_list = []
    for items in res2['data']:          # items是每一个需求
        for item in items:
            if item == "created_at":
                if seven_days_ago  > items[item]:
                    break
                else:
                    for item2 in items:
                        if item2 == 'id':
                            id = items[item2]
                            week_id_list.append(id)
                            break
                    break
    logging.info("week_id的长度为：{}".format(len(week_id_list)))
    print(week_id_list)  
    return week_id_list




def is_plan_completed(res3):
    """
    :type res3:dict
    :rtype:List
    判断该id是否完成了影响确认？
    """ 
    completed_list = []
    for item in res3['data']:
        for key in item:
            if key == "current_nodes":              # 完成的也就没有当前current_nodes参数了 
                print(type(item[key]))       # list[dict]
                for key1 in item[key]:
                    for key3 in key1:
                        # print(key3)
                        if key3 == "name":
                            if item[key][0][key3] != '方案影响确认':
                                for key2 in item:
                                    if key2 == 'id':
                                        completed_list.append(item[key2])
                                        break
                                break
                    break
                    
    logging.info("completed_id的长度为：{}".format(len(completed_list)))
    print(completed_list)
    return completed_list
    
                
            
def is_hil_test(res4):
    """
    :type res4:Json
    :rtype :List
    - 【需求类型】是【自定义测试流程】且【自定义测试内容】是【HIL测试】 template_id = 382839
    - 【需求类型】是【多模块功能变更提测流程】或者【Gate2.5提测流程】或者【Gate3/4提测流程】template_id= 348500/template_id= 379834/template_id= 379835
    """ 
    hil_test_id_list = []
    for item in res4['data']:
        item_id = 0
        for key in item:
            if key == 'id':
                item_id = item[key]
            if key == 'template_id':
                if item[key] == 348500 or item[key] == 379834 or item[key] == 379835:
                    if item_id != 0:
                        hil_test_id_list.append(item_id)
                        break
                    else:
                        for key1 in item:
                            if key1 == 'id':
                                hil_test_id_list.append(item[key1])
                                break
                if item[key] == 382839:
                    for key2 in item:
                        if key2 == 'fields':
                            for filed in item['fields']:      # string
                                if filed['field_key'] == "field_76ba38":
                                    for val in filed['field_value']:      # filed['filed_value] 是 list类型
                                        if 'label' in val and val['label'] == "HIL测试":
                                            if item_id != 0:
                                                hil_test_id_list.append(item_id)
                                                break
                                            else:
                                                for key3 in item:
                                                    if key3 == 'id':
                                                        hil_test_id_list.append(item[key3])
                                                        break
    logging.info("hil_test_id的长度为：{}".format(len(hil_test_id_list)))
    print(hil_test_id_list)
    return hil_test_id_list    
                                        
                                    
                            
                    
    

def commit_logsim_task():
    """
    :type author:str
    :type base_uuid:int
    :type diff_uuid:int
    :type task_name:str
    :type project:str
    :type module_type:List[str]
    """ 
    # 这部分要根据字段进行配置
    print("###########################要提交logsim任务####################################################")
    
    # version_type_list = []
    # if project == "NT2":
    #     version_type_list = type_list
    # if project == "ONVO":
    #     version_type_list.append('基础版')
        
    
    url = f"https://testeval.nio.com/silExternalInterface"
    data = {
        "sil_platform": "0", #测试时发1, 线上发0
            "data": {
                "type": "25",
                "data": {
                    "author": "zhenkai.shen.o@nio.com",  # 创建人邮箱，最好为可配置，现在默认都是zhenkai
                    "base_uuid": "12345",  #飞书项目里的【基准版本(Base)】字段的值
                    "diff_uuid": "123456",  # 飞书项目里的【bundle uuid】字段的值
                    "task_name": "lx_test001",  # 任务名称 飞书项目里的【名称】字段的值
                    "project": "NT2",  #  飞书项目里的【平台】字段的值，NT2发送“NT2”， ONVO发送“NT3”       
                    "module_type": ["AEB"],  # 飞书项目里的【执行功能】字段的值，列表
                    "version_type": ["基础版"],  # 如果【平台】是NT2根据【版本模式】选择, 如果【平台】是ONVO，默认是["基础版"]
                    "task_type": "全量测试",  # 任务类型，当前默认写【全量测试】
                    "plan_type": "纯logsim",  # 仿真模式，当前默认写【端到端】
                    "scene_id": []  # 场景库ID列表, 可为空，当前默认为空
                }
            }
    }

    header ={"Content-Type": "application/json"} 
    
    try:  
        # 发送POST请求，携带数据  
        response = requests.post(url, data=json.dumps(data),headers=header)  
          
        # 检查响应状态码  
        if response.status_code == 200:            # 这个返回的内容
              
            return response.text  # 返回响应内容  
        else:  
            return f"请求失败，状态码：{response.status_code}"  
    except requests.RequestException as e:  
        return f"请求异常：{e}" 
    
    

def get_feishu_docment(name,bundle_uuid,func_list,project):
    """ 
    :type name:str 
    :type bundle_uuid:int
    :type func_list :list
    :type project :str
    """
    app_id = 'cli_a3db4218543d500b'
    app_secret = 'VNCVqBsAXfg4IDfXScZPUgrVrv8Gu3eR'
    # 这个token需要更改为自己的，且他是更新的
   # app_token = 't-g1047ah2BJQKCG6Y7URZTPICXXPO4A3MYFZJR5JQ'          # t-g1047bcnS45XS7TWIMTRUHCIQF3EAR6ITAXLVSYZ
    app_token = 'XYjzbWDkva1W3IsyBz4cfjqWnPb'
    fs = FeishuBiTable(app_id, app_secret)


    filter_str = f'AND(' \
                f'CurrentValue.[NT2/NT3]="{project}"' \
                f',CurrentValue.[提测功能]="{func_list}"' \
                f',CurrentValue.[DiffUUID]="{bundle_uuid}"'\
                f')'
    print(filter_str)
    table_id = 'tblpn2Mzwmt3ejZS'
    data = fs.get_bitabl_record_list(app_token, table_id, filter_str=filter_str)
    
    if not data:
        logging.info("获取飞书文档失败")
  

    return data



  
    
           
          
    

def avoid_job_failed():
    """
    更新飞书项目字段，需要按照以下变更： 飞书项目空间 -> 具体的工作项 -> 具体的工作ID -> 具体字段的key；
    sdk和飞书项目api的调用方式可参考以下示例；
    """
    lpc = LarkClientSingleton("sj_test")  # 指定域名空间,相当于获取这个sj_test的一些密钥,创建了一个类LarkClientSingleton
    print(type(lpc))
    print(lpc)
    lpc.use_work_type("需求")  # 指定工作项类型        # 这个地方获取了api_name
    print("hello world")

    # 编辑目标字段
    """
    编辑目标字段
    field_key是要更改的字段的key
    work_item_id是工作项id
    """
    # update_fields = [{"field_key": "field_843eb2", "field_value": "51310453"}]
    # res = lpc.work_item_info().update_work_items_by_id(work_item_id=3976678257, update_fields=update_fields)
    # res = lpc.work_item_info().delete_work_items_by_id(work_item_id = 4423432073)
    
    # res = lpc.work_item_info().create_work_items('lx_002',4423432073)
    
    # res2 = lpc.work_item_info().get_assign_workitem(200)       # 现在这个地方请求页最大是200，需要进一步去解决。
    # id_list = get_all_id(res2)
    # week_id_list = get_week_id(res2)
    
    # 1. 获取指定工作项详情 测试代码
    # res = lpc.work_item_info().query_work_items_by_ids([4423434149])
    res = lpc.work_item_info().get_field_by_id(4423434149)
    
    with open('0708.json','w') as f:
        json.dump(res,f)
    f.close()
    
    
    # get_fields(res)       # 判断基本设置是否符合要求
    # res3 = lpc.work_item_info().query_work_items_by_ids(week_id_list)       # 这个res返回的是过去1周内所有的需求
    # completed_list = is_plan_completed(res3)                                # 在week_id_list中获取方案影响确认完成的id_list
    
    # res4 = lpc.work_item_info().query_work_items_by_ids([4423937751])       
    # hil_test_id_list = is_hil_test(res4)                                       # 在completed_list中判断哪些需要hil测试
    ############## 这个地方我感觉需要判断一下现在的结点 #################
    
    
    
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
                            "content": f"**：bundle_uuid不是纯数字**\n",
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
    jira_list = ['<at email=xin.lu2.o@nio.com></at>']
    # # jira_list = ['<at id=all>所有人</at>']
    # FM = FeishuMessage()
    # FM.message({'type': 'open_id', 'id': 'ou_b508c318c64f780f1ad98cd8015a2557'},'interactive',interactive) # 个人
    # FM.message({'type': 'chat_id', 'id': 'oc_218929f9da3f156359f451395254faaa'},'interactive',interactive) # 群聊
    
    
    
    
    # res = commit_logsim_task()
    # print(res)
    # name = "需求提测测试"
    # link = ""
    # res = get_feishu_docment(name = '需求提测测试',bundle_uuid = 2453288,func_list = 'AEB',project = 'NT2')
    # print(res)
    
    
    # for res_data in res:    # res_data是dict类型
    #     is_link = False
    #     for key in res_data['fields']:
    #         if key == '报告名称' and name in res_data['fields'][key][0]['text']:
    #             is_link = True
    #         if key == "报告链接" and is_link:
    #             link = res_data['fields'][key][0]['link']
        
           
    # print(link)
    
    # 更新文档
    # update_fields = [{"field_key": "description", "field_value": "https://nio.feishu.cn/record/Q3wYrWHPxeEQ2ScLUVLc7o49nFh"}]
    # lpc.work_item_info().update_work_items_by_id(4423434149, update_fields)
    # print(res)
    


if __name__ == "__main__":
    # schedule.every(1).minutes.do(avoid_job_failed)  
    
    # while True:  
    #     # 运行所有可以运行的任务  
    #     schedule.run_pending()  
    #     time.sleep(1)  # 减少CPU使用率，等待一秒
    avoid_job_failed()
    
    
    
    
    
    
    
