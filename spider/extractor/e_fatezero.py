from util.request_util import RequestUtil
from spider.extractor.abc_extractor import AbsExtractor
from util.ip_proxy import IpProxy
import json


class E_FatZero(AbsExtractor):
    """ FatZero """

    _SOURCE_DOMAIN = 'http://proxylist.fatezero.org/'

    _SOURCE_NAME = 'FatZero'

    def __init__(self):
        super().__init__()

    def extractor(self):
        """ http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = RequestUtil().get(url).text
            for each in resp_text.split("\n"):
                data = json.loads(each)
                proxy = IpProxy(data["host"], data["port"], [data["type"]], region=data["country"], anonymous="",
                                source=self._SOURCE_NAME, update_time="")
                yield proxy
        except Exception as e:
            print(e)


if __name__ == '__main__':
    e = E_FatZero()
    e.execute()