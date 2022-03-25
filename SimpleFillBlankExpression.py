# SFBEx
# 语法填空简写表达式（语填表达式）
## 用法
### 操作符
#### "~" 原样返回
##### (do)[~] -> (do)
#### "^" 首字母大写
##### (apple)[^] -> (Apple)
#### "-" 前/后缀（前缀在非单独存在和不会引起歧义的情况下可省略 "-"）
##### (relevant)[ir-] -> (irrelevant)
##### (link)[-s] -> (links)
##### (complicate)[un-d] -> (uncomplicated)
#### ">" 尾转换
##### (make)[e>ing] -> (making)
#### "=" 中间转换（向前匹配）
##### (stand)[an=oo] -> (stood)
##### (taxman)[a=e] -> (taxmen)
### 定界符
#### "|" 操作分区
##### (shake)[are |e>ing]/[are e>ing] -> (are shaking) {中间有空格，可省略}
##### (correct)[in|-ly]/[in-ly] -> (incorrectly) {第二操作由非字母开头，可省略，但不能写成 [in|ly] 等}
##### (able)[dis|le>ility]/[dis-le>ility] -> (disability) {第二操作由字母开头，不可省略写成 [disle>ility] 等}
## 规范
### 1. 仅允许出现字母、"~"、"^"、"-"、">"、"="、"|"
#### ×: (favour)[+ite] -> Error!
#### √: (favour)[-ite] -> (favourite)
### 2. 除 "^" 和 "|" 外，其它任意两个特殊符号不能连用
#### ×: (mature)[im--ly] -> Error!
#### √: (mature)[im-ly] -> (immaturely)
#### √: (additional)[^-ly] -> (Additionally)
#### √: (usual)[un-|-ly] -> (unusually)
### 3. "~" 必须单独存在
#### ×: (like)[~s] -> Error!
#### √: (like)[-s] -> (likes)
### 4. "^" 仅能出现在开头
#### ×: (evident)[-ly^] -> Error!
#### √: (evident)[^-ly] -> (Evidently)
### 5. 仅由字母构成的表达式视为「对原式的替换」
#### ×: (agree)[dis] -> (dis)
#### √: (agree)[dis-] -> (disagree)
### 6. 向后的处理必须先于向前的处理，例如前缀必须写在后缀前
#### ×: (legal)[-ly|il-]/[-ly|il] -> Error!
#### √: (legal)[il-ly]/[il-|-ly]/[il|-ly] -> (illegally)
### 7. "~", "^", "-", ">", "=" 均仅能使用一次

import re
from itertools import permutations

class ExpressionError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

def SFBEx(expression):
    try:
        if not len(expression):
            raise ExpressionError("Please give expression!")
        elif "~" in expression and len(expression) != 1:
            raise ExpressionError("\"~\" must be use alone!")
        elif not set(expression).issubset(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~^->=|")):
            raise ExpressionError("Unrecognizable metacharacter.")
        elif expression.count("^") and expression[0] != "^":
            raise ExpressionError("\"^\" must be use at the beginning!")

        for string in "^->=":
            if expression.count(string) >= 2:
                raise ExpressionError("\"" + string + "\" can be used only once!")
        for fbtup in list(permutations("->=", 2)):
            if "".join(fbtup) in expression:
                raise ExpressionError("\"" + fbtup[0] + "\" and \""  + fbtup[1] + "\" can not be adjacent!")
    except ExpressionError as Error:
        print("ExpressionError:", Error)
        exit()

SFBEx("-=")
print(1)