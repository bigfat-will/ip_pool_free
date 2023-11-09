from util.request_util import RequestUtil
from spider.extractor.abc_extractor import AbsExtractor
from util.ip_proxy import IpProxy


class E_Docip(AbsExtractor):
    """ 稻壳代理 """

    _SOURCE_DOMAIN = 'https://www.docip.net/'

    _SOURCE_NAME = '稻壳代理'

    def __init__(self):
        super().__init__()

    def extractor(self):
        """ 稻壳代理 https://www.docip.net/ """
        try:
            res = RequestUtil().get("https://www.docip.net/data/free.json", timeout=10)
            for data in res.json['data']:
                ip = data['ip'].split(":")
                protocol = ["HTTP", "HTTPS"] if data['proxy_type'] == 1 else ["HTTP"]
                proxy = IpProxy(ip[0], ip[1], protocol, region=data["addr"], anonymous="",
                                source=self._SOURCE_NAME, update_time="")
                yield proxy
        except Exception as e:
            print(e)
