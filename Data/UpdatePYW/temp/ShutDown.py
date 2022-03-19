"""
Adapted From https://www.cnblogs.com/summerise8090/p/8340070.html
"""

import tkinter.messagebox
from tkinter import *
from datetime import *
import os
from threading import *

window = tkinter.Tk()
window.withdraw()
tmNow = datetime.now()
d = date.today()
t = time(23, 0, 0)
shutdownTime = datetime.combine(d, t)

def Hint(tm):
    while True:
        tmNow = datetime.now()
        timedDelta = (shutdownTime - tmNow).total_seconds()
        if timedDelta <= tm:
            tkinter.messagebox.showwarning("自动关机提示", "距离关机还有 " + str(int(timedDelta)) + " 秒！请尽快处理必要事务，以免关机造成损失！")
            return

def ShutDown():
    while True:
        tmNow = datetime.now()
        timedDelta = (shutdownTime - tmNow).total_seconds()
        if timedDelta <= 301:
            os.system("shutdown -s -f -t " + str(int(timedDelta)))
            return

ShutDown()
for tm in [301, 181, 61]:
    Hint(tm)
window.destroy()