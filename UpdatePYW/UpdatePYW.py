"""
由于性能较差，故废弃
文件目录变更，已无法使用
"""

import os
import re
import time
import difflib
import filecmp
from datetime import datetime
from shutil import copy

def UpdatePYW(files, target):
    for file in files:
        file = os.path.join(os.path.split(os.path.abspath(__file__))[0], file)
        aim = target + re.sub("\.[a-z]+$", "", os.path.basename(file)) + "/"
        if not os.path.exists(aim):
            os.makedirs(aim)
        rfile = aim + os.path.basename(file) + "w"
        with open(file, encoding = "UTF-8") as ofile:
            content = ofile.read()
            with open(rfile, "w+", encoding = "UTF-8") as tfile:
                tfile.write(content)

def ReadFile(file):
    with open(file, "r", encoding = "UTF-8") as fileHandle:
        text = fileHandle.read().splitlines()
    return text

def Log(files):
    global target
    temptarget = os.path.join(target, "UpdatePYW", "temp")
    logstarget = os.path.join(target, "UpdatePYW", "logs")
    contrastarget = os.path.join(target, "UpdatePYW", "contrast")
    nowtime = datetime.now()
    now = nowtime.strftime("%Y-%m-%d_%H-%M-%S")
    for file in files:
        file = os.path.join(os.path.split(os.path.abspath(__file__))[0], file)
        if not filecmp.cmp(temptarget + os.path.basename(file), file):
            with open(os.path.join(logstarget, nowtime.strftime("%Y-%m-%d") + ".log"), "a+", encoding = "UTF-8") as logfile:
                tm = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                warning = "Please open \"" + now + "_" + os.path.basename(file) + ".html\" " + "in folder \"" + contrastarget + "\" to check details.\n\n"
                content = tm + "   " + os.path.basename(file) + " is modified.\n" + warning
                logfile.write(content)
            result = difflib.HtmlDiff().make_file(ReadFile(temptarget + os.path.basename(file)), ReadFile(file),temptarget + os.path.basename(file), file, context = True)
            with open(contrastarget + now + "_" + os.path.basename(file) + ".html", "w+", encoding = "UTF-8") as resultfile:
                resultfile.write(result)
            copy(file, temptarget)

files = [
    "UpdatePYW.py",
    "StartUp.py",
    "ShutDown.py",
]
target = os.path.join(os.path.split(os.path.abspath(__file__))[0], "Data")

while True:
    UpdatePYW(files, target)
    Log(files)
    time.sleep(28800)