"""
Adapted From https://www.cnblogs.com/oziasly/p/15257280.html
"""

import os
import pyautogui
import time
from datetime import datetime
import cv2

def ImgAutoClick(tempFile, whatDo, debug = False):
    pyautogui.screenshot("G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/StartUp/big.png")
    gray = cv2.imread("G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/StartUp/big.png", 0)
    img_template = cv2.imread(tempFile, 0)
    w, h = img_template.shape[::-1]
    res = cv2.matchTemplate(gray, img_template, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top = min_loc[0]
    left = min_loc[1]
    x = [top, left, w, h]
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    pyautogui.moveTo(top + h/2, left + w/2)
    whatDo(x)

    if debug:
        img = cv2.imread("G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/StartUp/big.png", 1)
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
        img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5, interpolation = cv2.INTER_NEAREST)
        cv2.imshow("processed", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    os.remove("G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/StartUp/big.png")

def SignIn(option, tm, aim, png):
    global now
    if now in tm:
        if "o" in option:
            os.startfile(aim)
        if "s" in option:
            time.sleep(10)
            ImgAutoClick(png, pyautogui.click, False)

target = "G:/Movable Computer/Library/ENoteBook/Assets/Tools/Data/StartUp/"
files = {
    "WeMeetApp": ["os", "12345", "D:/Program Files/Tencent/WeMeet/wemeetapp.exe"],
    "WeChat": ["os", "0123456", "D:/Program Files/WeChat/WeChat.exe"],
    "TIM": ["o", "0123456", "D:/Program Files/TIM/Bin/QQScLauncher.exe"],
}

now = datetime.now().strftime("%w")
for key, value in files.items():
    SignIn(value[0], value[1], value[2], target + key + ".png")