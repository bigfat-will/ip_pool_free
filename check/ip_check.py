# -*- coding: utf-8 -*-

import json
import time
from concurrent.futures import ThreadPoolExecutor
from util.ip_proxy import IpProxy
from requests import head
from db.db_client import DbClient

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Language': 'zh-CN,zh;q=0.8'}

HTTP_URL = "http://baidu.com"

HTTPS_URL = "https://baidu.com"


def proxy_validator(proxy):
    proxies = {"http": "http://{host}:{port}".format(host=proxy.host, port=proxy.port),
               "https": "https://{host}:{port}".format(host=proxy.host, port=proxy.port)
               }
    try:
        protocols = []
        for pro in proxy.protocol:
            if pro == 'HTTPS':
                r = head(HTTPS_URL, headers=HEADER, proxies=proxies, timeout=10, verify=False)
            else:
                r = head(HTTP_URL, headers=HEADER, proxies=proxies, timeout=10)

            if True if r.status_code == 200 else False:
                protocols.append(pro)

        return protocols
    except Exception as e:
        return []


class IPCheck:

    def __init__(self):
        self._client = DbClient()

    def proxy_check(self, proxy):
        protocols = proxy_validator(proxy)
        proxy.protocol = protocols
        proxy.update_time = time.time()
        if len(protocols) == 0:
            self._client.del_ip_proxy(proxy)
        else:
            self._client.save_ip_proxy(proxy)

    def check_thread_executor(self):
        with ThreadPoolExecutor(max_workers=10, thread_name_prefix='ip_check_pool') as executor:
            # 提交多个任务并并行执行
            for message in self._client.subscribe_tmp().listen():
                if message['type'] != 'message':
                    continue
                data = json.loads(message["data"])
                proxy = IpProxy(data["host"], data["port"], data["protocol"], data["region"], data["anonymous"],
                                data["source"])
                print("listen %s " % proxy.get_dict())
                executor.submit(self.proxy_check, proxy)
