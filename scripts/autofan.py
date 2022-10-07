#!/usr/bin/python3
# -*- coding: utf-8 -*-

import lgpio, re, os, subprocess, logging
from time import sleep
from pathlib import Path


def check_CPU_temp():
    t = 0
    err, msg = subprocess.getstatusoutput(
        "/usr/bin/zsh -c 'LD_LIBRARY_PATH=/opt/vc/lib /opt/vc/bin/vcgencmd measure_temp'"
    )
    if not err:
        m = re.search(r"-?\d\.?\d*", msg)  # a solution with a regex
        try:
            t = int(m.group())
        except ValueError:  # catch only error needed
            pass
    return t, msg


def HIGH_FLAG_callback(old, new):
    if new:
        lgpio.gpio_write(h, channel, 1)
        logger.info("Fan started.")
        Path(flag_file).touch()
        logger.info(("Wrote flag: %s") % flag_file)
        logger.info(("Current %s") % msg)
    else:
        lgpio.gpio_write(h, channel, 0)
        logger.info("Fan stopped.")
        os.remove(flag_file)
        logger.info(("Deleted flag: %s") % flag_file)
        logger.info(("Current %s") % msg)


class VariableListenedOnChange:
    def __init__(self, init_value):
        self._value = init_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        for callback in self._callbacks:
            callback(old_value, new_value)

    def register_callback(self, callback):
        self._callbacks.append(callback)


# Logger setup
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)
fileHandler = logging.FileHandler("/var/log/autofan.log", mode="w")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

h = lgpio.gpiochip_open(0)
channel = 14
start_temp = 50
end_temp = 43
show_info = True
flag_file = "/usr/local/IS_HIGH_FLAG"
is_high = VariableListenedOnChange(False)
is_high.register_callback(HIGH_FLAG_callback)

if os.path.exists(flag_file):
    lgpio.gpio_write(h, channel, 0)
    logger.info("Got IS_HIGH_FLAG, stopping fan for now just in case.")
    os.remove(flag_file)

try:
    while True:
        temp = open("/sys/class/thermal/thermal_zone0/temp")
        temp = int(temp.read()) / 1000
        msg = "%.1f ℃" % temp
        # temp, msg = check_CPU_temp()

        if temp > start_temp and not is_high.value:  # 当SoC温度超过启动阈值且风扇处于关闭状态
            is_high.value = True
            show_info = True

        elif temp < end_temp and is_high.value:  # 当SoC温度低于关闭阈值且风扇处于打开状态
            is_high.value = False
            show_info = True

        elif show_info:
            logger.info("Nothing to do, Skipping now...")
            logger.info(("Current %s") % msg)
            show_info = False

        sleep(10)  # 每隔10秒监控一次

except:
    lgpio.gpiochip_close(h)
    logger.info("Controller Closed.")

lgpio.gpiochip_close(h)
logger.info("Controller Closed.")
