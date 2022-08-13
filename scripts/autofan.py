#!/usr/bin/python3
# -*- coding: utf-8 -*-

import lgpio, re, os, subprocess, logging
from time import sleep


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


h = lgpio.gpiochip_open(0)
channel = 14
start_temp = 50
end_temp = 43
show_info = True
is_high = False

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

if os.path.exists("/usr/local/IS_HIGH_FLAG"):
    lgpio.gpio_write(h, channel, 0)
    logger.info("Fan started.")
    os.remove("/usr/local/IS_HIGH_FLAG")

try:
    while True:
        temp = open('/sys/class/thermal/thermal_zone0/temp')
        temp = int(temp.read()) / 1000
        msg = "%.1f ℃" % temp
        #temp, msg = check_CPU_temp()

        if temp > start_temp and not is_high:  # 当SoC温度超过启动阈值且风扇处于关闭状态
            lgpio.gpio_write(h, channel, 1)
            logger.info("Fan started.")
            logger.info(("Current %s") % msg)
            show_info = True
            is_high = True

        elif temp < end_temp and is_high:  # 当SoC温度低于关闭阈值且风扇处于打开状态
            lgpio.gpio_write(h, channel, 0)
            logger.info("Fan stopped.")
            logger.info(("Current %s") % msg)
            is_high = False
            show_info = True

        elif show_info:
            logger.info("Nothing to do, Skipping now...")
            logger.info(("Current %s") % msg)
            show_info = False

        sleep(10)  # 每隔10秒监控一次

except:
    lgpio.gpio_write(h, channel, 0)
    logger.info("Fan stopped.")
    lgpio.gpiochip_close(h)
    logger.info("Controller Closed.")

lgpio.gpiochip_close(h)
logger.info("Controller Closed.")
