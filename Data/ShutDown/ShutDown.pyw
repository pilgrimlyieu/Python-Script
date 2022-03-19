from datetime import datetime
from time import time, strptime, mktime, sleep
from os import system
from tkinter import Tk
from tkinter.messagebox import showwarning

def GetTime(clock):
    nowTime = datetime.now()
    specified_time = nowTime.strftime("%Y-%m-%d") + " {}:00:00".format(clock)
    timeArray = strptime(specified_time, "%Y-%m-%d %H:%M:%S")
    return mktime(timeArray)

interval = GetTime(23) - time()

def Hint():
    if interval < 180:
        return
    elif interval >= 300:
        sleep(interval - 300)
    window = Tk()
    window.withdraw()
    showwarning("自动关机提示", "距离关机还有 3 分钟！请尽快处理必要事务，以免关机造成损失！")
    sleep(120)
    showwarning("自动关机提示", "距离关机还有 1 分钟！请尽快处理必要事务，以免关机造成损失！")
    window.destroy()

def Shutdown():
    if interval < 180:
        system("shutdown -s -f -t 0")
        return
    elif interval >= 300:
        sleep(interval - 300)
    system("shutdown -s -f -t 299")
    return

Shutdown()
Hint()