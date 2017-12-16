from multiprocessing import Process
from subprocess import Popen
from contextlib import contextmanager
from time import sleep

from pydwm import init_dwm

from .status_bar import start as status_bar_start
from .status_bar import cpu as status_cpu
from .status_bar import mem as status_mem
from .status_bar import wifi as status_wifi
from .status_bar import vol as status_vol
from .status_bar import battery as status_battery
from .status_bar import datetime as status_datetime


PROCESSES = {
    'python': [
        'init_status_bar',
    ],
    'system': [
        ('syndaemon', '-i', '1', '-t', '-K'),
    ]
}


process_list = []


@contextmanager
def process_killer():
    yield

    for p in process_list:
        p.terminate()


def start():
    with process_killer():
        for p in PROCESSES['python']:
            process = Process(target=globals()[p])
            process.start()
            process_list.append(process)

        for p in PROCESSES['system']:
            process_list.append(
                Popen(p)
            )
        init_dwm()


def init_status_bar():
    conf = [
        {
            "sleep": 2,
            "callback": status_cpu,
        },
        {
            "sleep": 10,
            "callback": status_mem,
        },
        {
            "sleep": 3,
            "callback": status_wifi,
        },
        {
            "sleep": 1,
            "callback": status_vol,
        },
        {
            "sleep": 10,
            "callback": status_battery,
        },
        {
            "sleep": 1,
            "callback": status_datetime,
        },
    ]
    status_bar_start(conf)


start()
