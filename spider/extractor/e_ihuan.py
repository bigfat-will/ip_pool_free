from util.request_util import RequestUtil
from spider.extractor.abc_extractor import AbsExtractor
from util.ip_proxy import IpProxy


class E_Ihuan(AbsExtractor):
    """ 小幻代理 """

    _SOURCE_DOMAIN = 'https://ip.ihuan.me/address/5Lit5Zu9.html'

    _SOURCE_NAME = '小幻代理'

    def __init__(self):
        super().__init__()

    def extractor(self):
        """ 小幻代理 https://ip.ihuan.me/address/5Lit5Zu9.html
            有验证码，后面在弄
        """
        headers = {
            'Cookie': 'cf_chl_2=39b1b9f301fbbb4; cf_clearance=lbc2UL4D3N1sCI3dGb4a7AU9fMHUXc0fZSP64MV87d8-1699410415-0-1-953adbbb.f0bffe15.c23b845b-250.0.0; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1699410428; statistics=6bf9f47fa7833780f7fb47814ffc5090; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1699410813',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
        try:
            res = RequestUtil().tree("https://ip.ihuan.me/address/5Lit5Zu9.html", headers=headers, timeout=10)

            page_list = res.xpath('//ul[@class=pagination]//li//a/@href')
            for page in page_list:
                page_res = RequestUtil().tree("https://ip.ihuan.me/address/5Lit5Zu9.html", headers=headers, timeout=10)

                yield {}
        except Exception as e:
            print(e)


