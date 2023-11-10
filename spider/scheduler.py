# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from spider.extractor import _ALL_CLASSES
from check.ip_check import IPCheck
from db.db_client import DbClient
import datetime
import concurrent

TIMEZONE = "Asia/Shanghai"


def run_cla(cla):
    cla().execute()


def copy_check_thread_executor():
    DbClient().copy_proxy()


def run_check_thread_executor():
    IPCheck().check_thread_executor()


def spider_thread_executor():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10, thread_name_prefix='spider_pool') as executor:
        # 提交多个任务并并行执行
        all_task = [executor.submit(run_cla, cla) for cla in _ALL_CLASSES]
        # wait(all_task, timeout=1, return_when=ALL_COMPLETED)


def _scheduler():
    scheduler = BlockingScheduler()

    # 指定任务的运行时间，这里是当前时间之后的1秒
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    scheduler.add_job(run_check_thread_executor, 'date', run_date=run_time, id="ip_check_thread_executor",
                      name="check")

    scheduler.add_job(copy_check_thread_executor, 'interval', minutes=2, id="ip_check_copy_thread_executor",
                      name="check_copy")

    scheduler.add_job(spider_thread_executor, 'interval', minutes=1, id="spider_thread_executor",
                      name="spider")

    executors = {
        'default': ThreadPoolExecutor(max_workers=20),
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=TIMEZONE)

    scheduler.start()


if __name__ == '__main__':
    _scheduler()