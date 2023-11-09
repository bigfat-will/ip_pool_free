# -*- coding: utf-8 -*-


import json


class IpProxy(object):

    def __init__(self, host, port, protocol, region="", anonymous="",
                 source="", update_time=""):
        """
        :param host: ip
        :param port: 端口
        :param protocol: 协议类型数组 （http,https）
        :param region: 地理位置
        :param anonymous: 匿名
        :param source: 来源
        :param update_time: 更新时间
        """
        self.host = host
        self.port = port
        self.protocol = protocol
        self.region = region
        self.anonymous = anonymous
        self.source = source
        self.update_time = update_time

    def get_key(self):
        return "%s:%s" % (self.host, self.port)

    def get_dict(self):
        """ 属性字典 """
        return {"host": self.host,
                "port": self.port,
                "protocol": self.protocol,
                "region": self.region,
                "anonymous": self.anonymous,
                "source": self.source,
                "update_time": self.update_time
                }

    def get_json(self):
        """ 属性json格式 """
        return json.dumps(self.get_dict(), ensure_ascii=False)
