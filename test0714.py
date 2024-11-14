import requests
from client.lark_project_client import LarkClientSingleton
# from api.work_item_info import update_work_items_by_id
import json
import logging
import time
from typing import List
from feishu_api import *
from feishu_utils.feishu_message import FeishuMessage
from feishu_utils.feishu_sheets import FeishuSheets
import requests
import sys
import ast
import schedule



def get_manifest(uuid):
    """ 
    判断manifest是否已生成
    """
    url = f'https://mazu.nioint.com/api/p/v1/build/list?uuid={uuid}&limit=200'
    res = requests.get(url, headers={'x-userName': 'adsim'}).json()
    print(res)
    
    return res['data']


def get_fields(res:json):
    # print(type(res['data']))    # 这应该是个列表  list
    # print(len(res['data']))    # 1
    for item in res['data']:             # 这个item是每一个需求
        # print(type(item))      # dict
        is_warn = False
        name = ""
        id = 0
        for ite in item:
            if ite == 'name':
                name = item[ite]
                print("需求名称：",name)
            if ite == 'id':
                id = item[ite]
                print("id：",id)
                with open('warned_id.txt','r') as warn:
                    for line in warn:
                        print(line)
                        if str(id) in line:
                            is_warn = True
                            break
                warn.close()
        if is_warn:
            continue
            
        for it in item:
            if it == 'created_at':
                created_time = item[it]
                # print(type(created_time))       # int 
                print(created_time)
                
            if it == 'fields':
                for i in item['fields']:      # string
                    # print(i['field_key'])
                    # print(i)
                    if i['field_key'] == 'field_d97763':
                        bundle_uuid = i['field_value']
                        print(type(bundle_uuid))
                        bundle_uuid = bundle_uuid.replace('\n','')
                        isdight = bundle_uuid.isdigit()
                        print("bundle_uuid：",bundle_uuid)        # 这里面有换行符
   
                        # print(isdight)
                        if isdight:
                            print("您的需求{}bundle_uuid是纯数字".format(name))
                        else:
                            print("bundle_uuid不是纯数字")
                            with open('warned_id.txt','a') as warn1:
                                warn1.writelines(str(id))
                                warn1.writelines('\n')       
                            warn1.close()
                            
                            message = "您的需求{}：bundle_uuid不是纯数字,请尽快更改！".format(name)
                            seed_message(message,id)
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
                            with open('warned_id.txt','a') as warn2:
                                warn2.writelines(str(id))
                                warn2.writelines('\n')       
                            warn2.close()
                            message1 = "您的需求{}：base_version不是纯数字，请尽快更改！".format(name)
                            seed_message(message1,id)
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
                            with open('warned_id.txt','a') as warn3:
                                warn3.writelines(str(id))
                                warn3.writelines('\n')       
                            warn3.close()
                            message2 = "您的需求{}：不是默认场景集，请尽快更改！".format(name)
                            seed_message(message2,id)
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
    seven_days_ago = now_timestamp - 2 * 86400000 
    print(now_timestamp)
    print(seven_days_ago)
    # seven_days_ago = 1719504000000
    
    if 'data' not in  res2:
        logging.info("获得week_id_list为空")
        return []
    
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
                                        
                                        
def is_logsim_test(res4):
    """
    :type res4:Json
    :rtype :List
    - 【需求类型】是【自定义测试流程】且【自定义测试内容】是【logsim测试】 template_id = 382839
    - 【需求类型】是【多模块功能变更提测流程】或者【Gate2.5提测流程】或者【Gate3/4提测流程】template_id= 348500/template_id= 379834/template_id= 379835
    """
    
    if 'data' not in  res4:
        logging.info("需要进入logsim_test的需求为空")
        return []
    logsim_test_id_list = []
    for item in res4['data']:
        item_id = 0
        for key in item:
            if key == 'id':
                item_id = item[key]
            if key == 'template_id':
                if item[key] == 348500 or item[key] == 379834 or item[key] == 379835:
                    if item_id != 0:
                        logsim_test_id_list.append(item_id)
                        break
                    else:
                        for key1 in item:
                            if key1 == 'id':
                                logsim_test_id_list.append(item[key1])
                                break
                if item[key] == 382839:
                    for key2 in item:
                        if key2 == 'fields':
                            for filed in item['fields']:      # string
                                if filed['field_key'] == "field_76ba38":
                                    for val in filed['field_value']:      # filed['filed_value] 是 list类型
                                        if 'label' in val and val['label'] == "logsim测试":
                                            if item_id != 0:
                                                logsim_test_id_list.append(item_id)
                                                break
                                            else:
                                                for key3 in item:
                                                    if key3 == 'id':
                                                        logsim_test_id_list.append(item[key3])
                                                        break
    logging.info("logsim_test_id的长度为：{}".format(len(logsim_test_id_list)))
    print(logsim_test_id_list)
    return logsim_test_id_list  
    
    
                                    
                            
def is_commit_hil_or_logsim_task(res5,lpc):
    """
    :type res5: json
    :rtype :List
    """  
    for item in res5['data']:       # item就代表一个id的所有东西
        # 获取该id的所有信息
        id = 0
        author = ""              # 这个是提出者邮箱
        name = ""
        bundle_uuid = 0
        base_version = ""
        func_list = []
        project = ""
        version_type_list = []
        for key in item:
            if key == 'id':
                id = item[key]
            if key == "author":
                author = item[key]
            if key == "name":
                name = item[key]
            if key == "fields":   # 进入第二个字典中
                for it in item[key]:
                    if it['field_key'] == 'field_d97763':
                        bundle_uuid = it['field_value'] 
                        bundle_uuid = bundle_uuid.rstrip('\n')  # 需要把换行去掉
                        res_list = get_manifest(bundle_uuid)
                        if not res_list:
                            return None
                    if it['field_key'] == 'field_c7a8e8':
                        base_version = it['field_value']
                    if it['field_key'] == 'field_bf1d36':
                        for dic in it['field_value']: 
                            func_list.append(dic['label']) 
                    if it['field_key'] == "field_e4ca95":
                        project = it['field_value']['label']                  # project有问题
                    if it['field_key'] == 'field_0a903a':
                        for dic in it['field_value']:
                            version_type_list.append(dic["label"])
                    if it['field_key'] == 'priority':
                        priority = it['field_value']['label']
                        print("优先级：",priority)
                    
                        
                        
                
        # 'field_value': '基于周末伴生版本（v2）uuid: 2523121\n1. 基于stamp二轮优化 \n2. 后处理放出遮挡目标，将模型遮挡属性映射到遮挡率\n3.pnc这边 将30的遮挡率目标过滤，仅保留小于30，然后ped目标不过滤 \n\n kunyao/add_model_occ_in_blocked_parts\nintegration commit 929f0d44-https://ad-gitlab.nioint.com/ad/perception/engineering/external_group/argus_post_integration/-/commit/929f0d44293cde0e59e50d88a1acb5412c61a660 \naeb_30_fcw_mai\n'
        count = 0
        is_commit = False
        for key1 in item:
            if key1 == 'fields':
                for val2 in item[key1]:  # List[dict]      # val是字典
                    # print(val2['field_key'])
                    if val2['field_key'] == "field_e806a1": 
                        is_commit = True        
                        print(type(val2['field_value']))       # str
                        str1 = val2['field_value']
                        if 'http' in str1:
                            # 就代表已经提交了任务
                            break
                        else:
                            # 代表没有提交任务,在这个地方就要提交任务
                            # 获取创建人的邮箱，基准版本的id，bundle_uuid,name,project是NT2还是NT3？，执行功能；
                            with open('submitted_task_name.txt','r') as sub1:
                                for line in sub1:
                                    print(line)         # lx
                                    line = line.rstrip('\n')  
                                    print(type(line))
                                    print(name)        # lx_test002
                                    if line == name:            # 假如已提交，就直接这条id就不用提交了 
                                        return None
                            sub1.close()
                            count  = 1
                            commit_logsim_task(author=author,base_uuid=base_version,diff_uuid=bundle_uuid,task_name=name,project=project,module_type=func_list,type_list=version_type_list,priority = priority)
                            # 里面包含工作项id，已经更新内容
                            return [name,bundle_uuid,func_list,project,False]
                        
                # 这个地方假如没有这个字段，就代表没有提交过logsim任务
                if not is_commit:
                    with open('submitted_task_name.txt','r') as sub1: 
                        for line in sub1:
                            print(line)
                            print(type(line))
                            print(name)
                            if line == name:            # 假如已提交，就直接这条id就不用提交了 
                                return None
                    sub1.close()
                    count  = 1
                    commit_logsim_task(author=author,base_uuid=base_version,diff_uuid=bundle_uuid,task_name=name,project=project,module_type=func_list,type_list=version_type_list,priority = priority)
                    # 里面包含工作项id，已经更新内容
                    return [name,bundle_uuid,func_list,project,False]
    if count == 1:
        logging.info("{}:这条任务已提交".format(name))
    else:
        logging.info("{}:这条任务并没有走提交任务逻辑".format(name))
    return None
                            


    
      
    
           
def seed_message(message,id):
    """
    :type message: str
    :type id :int
    """    
    # 我要通过这个id获取是谁创建的
    # 根据id获取所有的解析文件，然后获得创建者，然后或者创建者id,然后发消息。id 是email。
    # 现在默认的都是写死的，都是发给我
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
                            "content": f"**{message}**\n",
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
                "content": f" 主动安全自动提测报警 ",
                "tag": "plain_text"
            }
        }
    }
    logging.info("已经收到该报警消息")
    jira_list = ['<at email=xin.lu2.o@nio.com></at>']
    # jira_list = ['<at id=all>所有人</at>']
    FM = FeishuMessage()
    FM.message({'type': 'open_id', 'id': 'ou_b508c318c64f780f1ad98cd8015a2557'},'interactive',interactive) # 个人
    # FM.message({'type': 'open_id', 'id': 'ou_819de01939ba6670a8f0885cc5e5aee7'},'interactive',interactive) # 个人    @ 雯姐的。
    # FM.message({'type': 'chat_id', 'id': 'oc_218929f9da3f156359f451395254faaa'},'interactive',interactive) # 群聊
    
             

def commit_logsim_task(author,base_uuid,diff_uuid,task_name,project,module_type,type_list,priority):
    """
    :type author:str
    :type base_uuid:int
    :type diff_uuid:int
    :type task_name:str
    :type project:str
    :type module_type:List[str]    func_list
    """ 
    # 这部分要根据字段进行配置
    print("###########################要提交logsim任务####################################################")
    
    if "ONVO" in project:    # project :\x08ONVO
        project = "NT3"
        type_list = ["基础版"]
    if priority == 'P0':
        priority_level = 1
    elif priority == 'P1' or priority == 'P2' :
        priority_level = 4
    else:
        priority_level = 7
    
    print(priority)
    print(priority_level)       # 优先级，data中加一下优先级就ok了
    
        
    
    url = f"https://testeval.nio.com/silExternalInterface"
    data = {
        "sil_platform": "0", #测试时发1, 线上发0
            "data": {
                "type": "25",
                "data": {
                    "author": "zhenkai.shen.o@nio.com",  # 创建人邮箱，最好为可配置，现在默认都是zhenkai
                    "base_uuid": base_uuid,  #飞书项目里的【基准版本(Base)】字段的值
                    "diff_uuid": diff_uuid,  # 飞书项目里的【bundle uuid】字段的值
                    "task_name": task_name,  # 任务名称 飞书项目里的【名称】字段的值
                    "project": project,  #  飞书项目里的【平台】字段的值，NT2发送“NT2”， ONVO发送“NT3”       
                    "module_type": module_type,  # 飞书项目里的【执行功能】字段的值，列表
                    "version_type": type_list,  # 如果【平台】是NT2根据【版本模式】选择, 如果【平台】是ONVO，默认是["基础版"]
                    "task_type": "全量测试",  # 任务类型，当前默认写【全量测试】
                    "plan_type": "端到端",  # 仿真模式，当前默认写【端到端】
                    "scene_id": [],  # 场景库ID列表, 可为空，当前默认为空
                    "priority":priority_level
                }
            }
    }
    print(data)

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
        logging.info("{}提交logsim任务失败".format(task_name))
        seed_message("{}提交logsim任务失败".format(task_name),"xin.lu2.o@nio.com")    # 这个对应的任务要发给对应的人 
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
           
    app_token = 'XYjzbWDkva1W3IsyBz4cfjqWnPb'        
    fs = FeishuBiTable(app_id, app_secret)
    if "ONVO" in project:    # project :\x08ONVO
        project = "NT3"


    link_list = []
    for func in func_list:                                  # 这个地方还有基础版和增强版两种
        filter_str = f'AND(' \
                     f'CurrentValue.[NT2/NT3]="{project}"' \
                     f',CurrentValue.[DiffUUID]="{bundle_uuid}"' \
                     f',CurrentValue.[提测功能]="{func}"' \
                     f')'

        table_id = 'tblpn2Mzwmt3ejZS'
        res = fs.get_bitabl_record_list(app_token, table_id, filter_str=filter_str)
            
            
        if not res:
            logging.info("获取飞书文档失败")
            # seed_message("获取报告失败","xin.lu2.o@nio.com")       # 默认先发给我
            return None
        print(res)
        # 假如检测到任务状态不是start/finish的话，就报警，然后把提交任务里面的名称删除，保证不在重复查询
        
        
        for res_data in res:    # res_data是dict类型
            
            for key1 in res_data['fields']:
                if key1 == 'Base任务状态':
                    if res_data[key1] != 'START' or res_data[key1] != 'FINISH' or res_data[key1] != 'EXEC':
                        logging.info("{}任务执行失败，请尽快处理，连接为".format(name))
                        seed_message("{}任务执行失败，请尽快处理,链接为{}".format(name,'https://nio.feishu.cn/base/XYjzbWDkva1W3IsyBz4cfjqWnPb?table=tblpn2Mzwmt3ejZS&view=vewbpqc8kG'),1)
                        delete_submitted_task(name)
                        return None
            is_link = False
            for key in res_data['fields']:
                if key == '报告名称' and name in res_data['fields'][key][0]['text']:
                    link_list.append(res_data['fields'][key][0]['text'])
                    is_link = True
                if key == "报告链接" and is_link and res_data['fields'][key] != None:
                    link_list.append(res_data['fields'][key][0]['link'])           # 'NoneType' object is not subscriptable

    if not link_list:
        return None
 
    update_content = [{"field_key": "field_e806a1", "field_value": str(link_list)}]          # link是一个列表list[str],测试一下这个什么结果
    return update_content

    
def delete_submitted_task(name):
    """
    1.删除已经获得报告的提交任务
    """  
    with open('submitted_task.txt','r') as task:
        lines_to_keep = [line for line in task if name not in line]  
        print(lines_to_keep)
    task.close()
    
    with open('submitted_task.txt','w') as task1:
        for line in lines_to_keep:
            task1.writelines(line)
    task1.close()  
    
          
    

def avoid_job_failed():
    """
    更新飞书项目字段，需要按照以下变更： 飞书项目空间 -> 具体的工作项 -> 具体的工作ID -> 具体字段的key；
    sdk和飞书项目api的调用方式可参考以下示例；
    """
    # lpc = LarkClientSingleton("sj_test")  # 指定域名空间,相当于获取这个sj_test的一些密钥,创建了一个类LarkClientSingleton
    # print(type(lpc))
    # print(lpc)
    # lpc.use_work_type("需求")  # 指定工作项类型        # 这个地方获取了api_name
    # print("hello world")

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
    
    
    
    
    
    # res2 = lpc.work_item_info().get_assign_workitem(100)            # 现在这个地方请求页最大是200，需要进一步去解决。
    # week_id_list = get_week_id(res2)
    
    
    # # 1. 获取指定工作项详情 测试代码
    # # res = lpc.work_item_info().query_work_items_by_ids([4423937751])
    # # with open('0708.json','w') as f:
    # #     json.dump(res,f)
    # # f.close()
    
    # # 判断基本设置是否符合要求
    # # week_id_list = [4446640989]
    # res3 = lpc.work_item_info().query_work_items_by_ids(week_id_list)       # 这个res返回的是过去1周内所有的需求
    # # get_fields(res3)                                                        # check字段
    # completed_list = is_plan_completed(res3)                                # 在week_id_list中获取方案影响确认完成的id_list
    
    # with open('warned_id.txt','r') as stop: 
    #     for line in stop:
    #         line = line.rstrip('\n')  
    #         if not line.isdigit():
    #             continue     
    #         if int(line) in completed_list:                                     #这个地方有问题
    #             completed_list.remove(int(line))
    # stop.close()
        
    # print(completed_list)       
    # if not completed_list:
    #     logging.info("这轮没有进入logsim/hil测试的需求")
    #     sys.exit(0)
    
    
    # res4 = lpc.work_item_info().query_work_items_by_ids(completed_list)     # 这个地方有请求
    # logsim_test_id_list = is_logsim_test(res4) 
    # res5 = lpc.work_item_info().query_work_items_by_ids(logsim_test_id_list)
    # get_fields(res5)  
    
    # # hil测试   
    # # hil_test_id_list = is_hil_test(res4)                                       # 在completed_list中判断哪些需要hil测试
    # ############## 这个地方我感觉需要判断一下现在的结点 #################
    # # res5 = lpc.work_item_info().query_work_items_by_ids(hil_test_id_list)
    # # hil_task_list = is_commit_hil_task(res5) 
    
    
    
    
    
    # # logsim测试
    # # logsim_test_id_list = [4455831185]
    # for id in logsim_test_id_list:
    #     res5 = lpc.work_item_info().query_work_items_by_ids([id])
    #     with open('0708.json','w') as f:
    #         json.dump(res5,f)
    #     f.close()

    #     task_list = is_commit_hil_or_logsim_task(res5,lpc)                   # 这个地方就是就是获取提交logsim任务的函数中的内容
    #     if task_list == None:
    #         continue
        
    #     with open ('submitted_task_name.txt','a') as sub:                # 代表将提交任务的name加入到文件里，加入已提交就不会重复提交了
    #         sub.writelines(str(task_list[0]))
    #         sub.writelines('\n')
    #     sub.close()
    
    
    #     # 从文件读取提交过的任务，然后get文档
    #     # task_list = [name,bundle_uuid,func_list,project,False]
    #     with open('submitted_task.txt','a') as task:
    #         task.writelines(str(task_list))
    #         task.writelines('\n')
    #     task.close()
         
    # with open('submitted_task.txt','r') as task1:
    #     for line in task1:
    #         vals = ast.literal_eval(line) 
    #         if not vals[4]:                     # False
    #             update_content = get_feishu_docment(vals[0],vals[1],vals[2],vals[3])
    #             if update_content == None:
    #                 logging.info("{}任务的测试报告还没有生成".format(vals[0]))
    #                 continue
    #         else:
    #             lpc.work_item_info().update_work_items_by_id(id,update_content)         # 更新内容 ，这个id是不是现在还没有获得，周一看一下。
    #             # vals[4] = True
    #             # 这个地方要更新文档，
    #             delete_submitted_task(vals[0])
    # task1.close()

    # res_list = ['bugfix 主线版本预埋vision_god链路对source_lidar目标输出vision_god结构_2600855_OAA_07172044', 'https://nio.feishu.cn/base/OV81b213eaNk0os19UHc5LTincc?table=tblvuenQ124WRglR&view=vewWxj7N0c','nam1111111111111111111','success']
    # str1 = 'bugfix 主线版本预埋vision_god链路对source_lidar目标输出vision_god结构_2600855_OAA_07172044\n' + 'https://nio.feishu.cn/base/OV81b213eaNk0os19UHc5LTincc?table=tblvuenQ124WRglR&view=vewWxj7N0c\n' + 'nam1111111111111111111\n'
    
    # # json_str = json.dumps(filed_value,indent= 4) 
    # val = ""
    # count = 0
    # for link in res_list:
    #     count += 1
    #     val += link
    #     if count % 2 == 0:
    #         val += '\n'
    #         val += '\n'
    #     val += '\n'

    # update_content = [{"field_key": "field_e806a1", "field_value": val}]
    
    # lpc.work_item_info().update_work_items_by_id(4468466382,update_content)
    # vals = '【纯视觉】透传s\\x08tamp_v'
    # for i in range(len(vals)-1):
    #     print(vals[i])
    # res = lpc.work_item_info().query_work_items_by_ids([4464977319])
    # with open('0709.json','w') as f:
    #     json.dump(res,f,ensure_ascii=False,indent = 4)
    # f.close()
    
    with open('warned_id.txt','r') as peron_do:
        for line in peron_do:
            print(line)
    peron_do.close()
    

    
        
    
    
    
    """
    1. 需要判断一下现在的结点状况，因为假如hil测试已完成，但是正在logsim结点上，现在的代码逻辑应该会把hil和logsim都会捞出来。
    2. 首先判断一下现在的结点逻辑。就是hil测试结点和logsim结点是否完成。不完成才会加入列表
    3. 每隔15分钟提交一次任务
    4. 加log,每个函数最起码有一个log
    5. 不能重复提交logsim任务,我要先获得logsim任务   done
    6. 测试一下回填logsim任务是否ok?   done
    7. 测试一下完整的流程线
    8. 给个人报警这个地方最后搞一下。   
    9. logsim测试报告这个关键字可能会没有，以及owner的关键字，这个地方需要解决。   done
    10. 测试一下get不到直接写的情况是否ok？        // 重复提交的任务问题已解决，done
    11. 搞一下重复发消息      重复报警的问题已解决
    12. 文档的名字已加：done
    13. bundle_uuid // base_version不是纯数字的是不是不能提交任务？
    14. 现在存在一个问题是假如bundle_uuid非法，我就拦截了，但是后面他改了的话，我也提交不了任务了。
    """
    
    

if __name__ == "__main__":
    # schedule.every(15).minutes.do(avoid_job_failed)  
    
    # while True:  
    #     # 运行所有可以运行的任务  
    #     schedule.run_pending()  
    #     time.sleep(1)  # 减少CPU使用率，等待一秒
    avoid_job_failed() 
    
    
