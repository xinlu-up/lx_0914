import requests
import time
import logging
import curlify


class HttpClient:
    def __init__(self, max_retries, retry_delay, api_host):
        self.api_host = api_host
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.headers = {'Content-type': 'application/json'}
        self.logger = logging.getLogger('HttpClient')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send_request(self, method, path, params=None, data=None, headers=None, timeout=30):       # get,path
        url = f"{self.api_host}{path}"           # URL ='https://project.feishu.cn/open_api/sj_test/work_item/all-types'
        
        # url = 'https://project.feishu.cn/sj_test/story/homepage'
        
        retries = 0
        headers = headers or self.headers
        while retries < self.max_retries:
            try:
                resp = requests.request(method=method, url=url, params=params, json=data, headers=headers,timeout=timeout)    # 这个地方出了问题
                print(resp)     # 401
                self.logger.info("CURL: {}".format(curlify.to_curl(resp.request)))
                resp.raise_for_status()                                  # 直接跳到了下面的抛错误地方  --> 31行
                # self.logger.info(f"Request successful {path}: {resp.text}")
                return resp
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e} \nresponse: {resp.text}")
                retries += 1
                if retries < self.max_retries:
                    self.logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)

        self.logger.error("Max retries reached. Request failed")
        return resp
