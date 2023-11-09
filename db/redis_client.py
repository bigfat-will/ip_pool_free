# -*- coding: utf-8 -*-

from redis import Redis
from redis.connection import BlockingConnectionPool


class RedisClient(object):
    """
    Redis client
    """

    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.__conn = Redis(connection_pool=BlockingConnectionPool(decode_responses=True,
                                                                   timeout=5,
                                                                   # socket_timeout=5,
                                                                   **kwargs))

    def expire(self, name, expire_time):
        self.__conn.expire(name, expire_time)

    def publish(self, topic, message):
        """
        返回所订阅频道
        :param topic:
        :return:
        """
        return self.__conn.publish(topic, message)

    def pubsub(self):
        """
        返回所订阅频道
        :param topic:
        :return:
        """
        return self.__conn.pubsub()

    def hset(self, name, key, value):
        data = self.__conn.hset(name, key, value)
        return data

    def hget(self, name, key):
        return self.__conn.hget(name, key)

    def hmget(self, name, keys):
        return self.__conn.hmget(name, keys)

    def hgetall(self, name):
        return self.__conn.hgetall(name)

    def hdel(self, name, key):
        self.__conn.hdel(name, key)

    def zadd(self, name, value, score):
        self.__conn.zadd(name, {value: score})

    def zrem(self, name, value):
        self.__conn.zrem(name, value)

    def zrevrange(self, name, start, stop):
        return self.__conn.zrevrange(name, start, stop)