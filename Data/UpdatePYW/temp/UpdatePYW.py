import os
import re
import time
import difflib
import filecmp
from datetime import datetime
from shutil import copy

def UpdatePYW(files, target):
    for file in files:
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
    temptarget = "G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/UpdatePYW/temp/"
    logstarget = "G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/UpdatePYW/logs/"
    contrastarget = "G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/UpdatePYW/contrast/"
    nowtime = datetime.now()
    now = nowtime.strftime("%Y-%m-%d_%H-%M-%S")
    for file in files:
        if not filecmp.cmp(temptarget + os.path.basename(file), file):
            with open(logstarget + nowtime.strftime("%Y-%m-%d") + ".log", "a+", encoding = "UTF-8") as logfile:
                tm = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                warning = "Please open \"" + now + "_" + os.path.basename(file) + ".html\" " + "in folder \"" + contrastarget + "\" to check details.\n\n"
                content = tm + "   " + os.path.basename(file) + " is modified.\n" + warning
                logfile.write(content)
            result = difflib.HtmlDiff().make_file(ReadFile(temptarget + os.path.basename(file)), ReadFile(file),temptarget + os.path.basename(file), file, context = True)
            with open(contrastarget + now + "_" + os.path.basename(file) + ".html", "w+", encoding = "UTF-8") as resultfile:
                resultfile.write(result)
            copy(file, temptarget)

files = [
    "G:/Movable Computer/Library/ENoteBook/Assets/Tools/UpdatePYW.py",
    "G:/Movable Computer/Library/ENoteBook/Assets/Tools/StartUp.py",
    "G:/Movable Computer/Library/ENoteBook/Assets/Tools/ShutDown.py",
]
target = "G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/"

while __name__ == "__main__":
    UpdatePYW(files, target)
    Log(files)
    time.sleep(28800)