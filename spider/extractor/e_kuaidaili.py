from util.request_util import RequestUtil
from spider.extractor.abc_extractor import AbsExtractor
from util.ip_proxy import IpProxy


class E_KuaiDaiLi(AbsExtractor):
    """ 快代理 """

    _SOURCE_DOMAIN = 'https://www.kuaidaili.com'

    _SOURCE_NAME = '快代理'

    def __init__(self):
        super().__init__()

    def extractor(self):
        """ 快代理 """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        try:
            for page_index in range(1, 3):
                for pattern in url_pattern:
                    url_list.append(pattern.format(page_index))

            for url in url_list:
                tree = RequestUtil().get(url).tree
                proxy_list = tree.xpath('.//table//tr')

                for tr in proxy_list[1:]:
                    print(tr.xpath('./td/text()'))
                    data = tr.xpath('./td/text()')
                    proxy = IpProxy(data[0], data[1], [data[3]], region=data[4], anonymous="",
                                    source=self._SOURCE_NAME, update_time="")
                    yield proxy
        except Exception as e:
            print(e)


if __name__ == '__main__':
    e = E_KuaiDaiLi()
    e.execute()