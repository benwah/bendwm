#!/usr/bin/env python

from threading import Thread, Lock, Event
import signal
import subprocess
import psutil
import re
import time

mutex = Lock()
thread_data = []


class UpdaterThread(Thread):
    def __init__(self, id, sleep, callback):
        Thread.__init__(self)
        self.stopped = Event()
        self.id = id
        self.sleeptime = sleep
        self.callback = callback

    def stop(self):
        self.stopped.set()

    def run(self):
        thread_data[self.id] = self.callback()
        with mutex:
            update()
        while not self.stopped.is_set():
            flagged = self.stopped.wait(
                self.sleeptime
            )
            if not flagged:
                thread_data[self.id] = self.callback()
                with mutex:
                    update()


def update():
    subprocess.call([
        "xsetroot",
        "-name",
        " | ".join(thread_data)
    ])


def start(conf):
    threads = []
    for i in range(len(conf)):
        thread_data.append("...")
        t = UpdaterThread(
            i,
            conf[i]['sleep'],
            conf[i]['callback']
        )
        t.setDaemon(True)
        threads.append(t)
    for t in threads:
        t.start()
    try:
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        print("stopping threads")
        for t in threads:
            t.stop()
        for t in threads:
            t.join()
        print("bye!")
        return 0


def datetime():
    return "".join([' ', time.strftime("%m-%d-%y - %H:%M:%S"), ' '])


def wifi():
    dev = "wlp2s0"
    wifi_info = open("/proc/net/wireless").read()
    signal_strength = 0
    try:
        essid = re.sub(
            r'^.*"([^"]*).*"',
            r'\1',
            str(subprocess.check_output(
                ["iwgetid"],
                shell=False
            ).strip())
        )
    except:
        essid = "(x)"
    try:
        signal_strength = int(int(
            re.findall(r'{}:\s*\S*\s*(\d*)'.format(dev), wifi_info)[0]
        ) / 70.0 * 100)
    except:
        signal_strength = 0
    output = ['wi: ']
    output.append('({}) '.format(essid))
    output.append('{}'.format(percent(signal_strength)))
    return "".join(output)


def battery():
    acpath = "/sys/class/power_supply/AC0"
    batpath = "/sys/class/power_supply/BAT0"
    ac_online = int(open(acpath+'/online', 'r').read().strip())
    max = int(open(batpath+'/energy_full', 'r').read().strip())
    cur = int(open(batpath+'/energy_now', 'r').read().strip())
    pct = int(100*float(cur)/float(max))
    output = ['bat: ']
    output.append("{}".format(percent(pct)))
    output.append("(")
    if ac_online:
        if pct == 100:
            output.append("+")
        else:
            output.append("~")
    else:
        output.append("-")
    output.append(")")
    return "".join(output)


def cpu():
    cpus = psutil.cpu_percent(interval=.5, percpu=True)

    mhz = re.search(
        "cpu MHz\s*:\s*(\S*)",
        open('/proc/cpuinfo', 'r').read()
    ).groups()[0].split('.')[0]

    output = [' cpu: ']
    output.append('{}Mz'.format(mhz))
    output.append('(')
    cpu_data = " ".join(map(lambda x: percent(int(x)), cpus))
    output.append(cpu_data)
    # for c in cpus:
    #     output.append('{}'.format(percent(int(c))))
    #     #output.append("{0: >3}% ".format(int(c)))
    output.append(')')
    return "".join(output)


def mem():
    minfo = psutil.virtual_memory()
    output = ['mem:']
    output.append("{0: >3}%".format(int(minfo.percent)))
    return "".join(output)


def vol():
    mixerinfo = subprocess. \
      check_output(['amixer', 'get', 'Master'], shell=False). \
      decode('utf-8'). \
      split('\n')[-2]
    master_vol = int(re.search(r'\[(\d*)%\]', mixerinfo).groups()[0])
    muted = re.search(r'\[(on|off)\]', mixerinfo).groups()[0]
    output = ['vol: ']
    output.append("{}".format(percent(master_vol)))
    if muted == 'off':
        output.append('M')
    return "".join(output)


def percent(pct=0):
    return "{pct}%".format(pct=pct)
