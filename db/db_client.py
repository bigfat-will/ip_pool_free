# -*- coding: utf-8 -*-
import json

import setting
from db.redis_client import RedisClient
from util.singleton_meta import SingletonMeta


class DbClient(metaclass=SingletonMeta):
    """
    DbClient DB工厂类
    """

    def __init__(self):
        """
        init
        :return:
        """
        self.name = "ip_proxy"
        self.name_tmp = "ip_proxy_tmp"
        self.expire_time = 24*60*60
        self.client = RedisClient(host=setting.REDIS_HOST,
                                  port=setting.REDIS_PORT,
                                  password=setting.REDIS_PASSWORD,
                                  db=setting.REDIS_DB
                                  )

    def copy_proxy(self):
        all = self.client.hgetall(self.name)
        for key, value in all.items():
            self.client.publish(self.name_tmp, value)

    def subscribe_tmp(self):
        pubsub = self.client.pubsub()
        pubsub.subscribe(self.name_tmp)
        return pubsub

    def save_ip_proxy_tmp(self, proxy):
        self.client.publish(self.name_tmp, proxy.get_json())

    def save_ip_proxy(self, proxy):
        self.client.hset(self.name, proxy.get_key(), proxy.get_json())
        self.client.expire(self.name, self.expire_time)

        for pro in proxy.protocol:
            l_key = "%s:%s" % (self.name, pro)
            self.client.zadd(l_key, proxy.get_key(), proxy.update_time)
            self.client.expire(l_key, self.expire_time)

    def del_ip_proxy(self, proxy):
        self.client.hdel(self.name, proxy.get_key())

        for pro in ["HTTP", "HTTPS"]:
            l_key = "%s:%s" % (self.name, pro)
            self.client.zrem(l_key, proxy.get_key())

    def get_ip_list(self, protocol="HTTP", start=0, stop=10):
        l_key = "%s:%s" % (self.name, protocol)
        key_list = self.client.zrevrange(l_key, start, stop)
        data_list = self.client.hmget(self.name, key_list)
        proxy_list = []
        for data in data_list:
            proxy = json.loads(data)
            del proxy['anonymous']
            del proxy['source']
            proxy_list.append(proxy)

        return proxy_list

