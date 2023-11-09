# -*- coding: utf-8 -*-


import click
from spider.scheduler import _scheduler
from api.api import run

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="1.0.0")
def _click():
    """"""

@_click.command(name="schedule")
def schedule():
    _scheduler()


@_click.command(name="api")
def server():
    run()


if __name__ == '__main__':
    _click()



