from abc import ABC, abstractmethod
from db.db_client import DbClient


class AbsExtractor(ABC):

    _SOURCE_DOMAIN = ''

    _SOURCE_NAME = ''

    def __init__(self):
        self._RESULT_LIST = []
        self._client = DbClient()

    @abstractmethod
    def extractor(self):
        pass

    def execute(self):
        print("spider init -- %s" % self._SOURCE_DOMAIN)
        for proxy in self.extractor():
            self.add_result(proxy)
        self.print_result()
        self.save_result()
        print("spider end -- %s" % self._SOURCE_DOMAIN)

    def add_result(self, res):
        self._RESULT_LIST.append(res)

    def save_result(self):
        for proxy in self._RESULT_LIST:
            self._client.save_ip_proxy_tmp(proxy)

    def print_result(self):
        for r in self._RESULT_LIST:
            print(r.get_dict())
