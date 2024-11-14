import requests
import json

_url = "https://aip.nioint.com/api/metrics/metrics/hil/sim/page/query?page_size=20&page=0&region=&report_type=&created=0"

_headers = {'Content-Type': 'application/json',"cookie":'lap.sid=s%3AkcK84Q5ctgwlm-EeZduzhJot9KqFR8uD.SbqICvV5K9s9zZQzqmi4qWR6MxOi60zWNpuJtESA72Q'}

# uuid_list = []
# uuid_list.append(uuid)
_body = {
    "page_size": 20,
    "page": 0,
    "created": 0
}


res = requests.get(_url,json.dumps(_body), headers=_headers)
# print(res.json())

with open('0905.json','w') as f:
    json.dump(res.json(),f,indent=4)
f.close()


res_list = res.json()['data']['content']
print(type(res_list))      # list

for res1 in res_list:
    # print(res1['test_target'])
    if '4893219558' in res1['test_target']:
        url = 'https://aip.nioint.com/#/adsim/hilSim/management/report?id=' + res1['id']
        print(url)
        break
        # return url
