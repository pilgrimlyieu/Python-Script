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
##### (correct)[in-|-ly]/[in|-ly]/[in-ly] -> (incorrectly) {第二操作由非字母开头，可省略，但不能写成 [in|ly] 等}
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
### 7. 除非严格模式下的 "-" 能使用两次（通过 "|"）和非严格模式下的 "|" 外，其他符号均仅能使用一次
### 8. word 仅由小写字母构成
### 9. 严格模式不支持 "|"
### 10. 严格模式不支持多后缀语法

import re
from itertools import permutations

class ExpressionError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

class WordError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

def isletter(string):
    return set(string).issubset("abcdefghijklmnopqrstuvwxyz")

def isvalid(string):
    return set(string).issubset("abcdefghijklmnopqrstuvwxyz ")

def SFBEx(word, expression = "~", strict = True):
    if isletter(expression):
        return expression
    try:
        if not isletter(word):
            raise WordError("Invalid word!")

        if not len(expression):
            raise ExpressionError("Please give expression!")
        elif "~" in expression and len(expression) != 1:
            raise ExpressionError("\"~\" must be use alone!")
        elif strict and "|" in expression:
            raise ExpressionError("Strict mode doesn't support \"|\" syntax!")
        elif strict and len(set(expression) & set("->=")) >= 2:
            raise ExpressionError("Strict mode doesn't support more than one suffix syntax!")
        elif not set(expression).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~^->=| "):
            raise ExpressionError("Unrecognizable metacharacter.")
        elif expression.count("^") and expression[0] != "^":
            raise ExpressionError("\"^\" must be use at the beginning!")

        if expression.count("-") >= 3:
            raise ExpressionError("\"-\" can be used twice at most!")
        for string in "^>=":
            if expression.count(string) >= 2:
                raise ExpressionError("\"" + string + "\" can be used only once!")
        for fbtup in list(permutations("->=", 2)):
            if "".join(fbtup) in expression:
                raise ExpressionError("\"" + fbtup[0] + "\" and \""  + fbtup[1] + "\" can not be adjacent!")
    except WordError as Error:
        print("WordError:", Error)
        exit()
    except ExpressionError as Error:
        print("ExpressionError:", Error)
        exit()

    parts = expression.split("|")
    wordlist = list(word)
    updone = not expression.count("^")
    beforedone = 0
    afterdone = 0

    for part in parts:
        try:
            if isvalid(part) and beforedone:
                raise ExpressionError("Can not give more than one prefix!")
        except ExpressionError as Error:
            print("ExpressionError:", Error)
            exit()
        if isvalid(part) and not beforedone:
            wordlist = list(part) + wordlist
            beforedone = 1

        partplus = list(part)
        partplus.append("!")
        dotype = "no"
        beforetemp = []
        begin = 0
        end = 0

        for unit in range(0, len(partplus)):
            if not updone:
                wordlist[0] = wordlist[0].upper()
                updone = 1
                begin = 1
                continue

            if not isvalid(partplus[unit]):
                end = unit
                if dotype == ">":
                    try:
                        if wordlist[-len(beforetemp):] != beforetemp:
                            raise ExpressionError("The first parameter given by \">\" is invalid!")
                    except ExpressionError as Error:
                        print("ExpressionError:", Error)
                        exit()
                    del wordlist[-len(beforetemp):]
                    wordlist.extend(list(part[begin:end]))
                    dotype = "no"
                    afterdone = 1
                elif dotype == "=":
                    try:
                        if "".join(beforetemp) not in "".join(wordlist):
                            raise ExpressionError("The first parameter given by \"=\" is nonexistent!")
                    except ExpressionError as Error:
                        print("ExpressionError:", Error)
                        exit()
                    wordlist = wordlist[:"".join(wordlist).rfind("".join(beforetemp))] + list(part[begin:end]) + wordlist["".join(wordlist).rfind("".join(beforetemp)) + len(beforetemp):]
                    dotype = "no"
                    afterdone = 1
                elif dotype == "-":
                    if len(set(">=") & set(partplus)) == 0:
                        wordlist.extend(list(part[begin:end]))
                        dotype = "no"
                    else:
                        temp = -1
                        if ">" in partplus and "".join(partplus).index(">") > unit:
                            temp += 1
                        elif "=" in partplus and "".join(partplus).index("=") > unit:
                            temp += 1
                        if temp == 1:
                            wordlist.extend(list(part[begin:end]))
                            dotype = "no"
                            temp = -1

                if partplus[unit] in ">=":
                    try:
                        if begin >= end:
                            raise ExpressionError("Please give string to be replaced via \"" + partplus[unit] + "\"!")
                    except ExpressionError as Error:
                        print("ExpressionError:", Error)
                        exit()
                    beforetemp = partplus[begin:end]
                    begin = unit
                elif partplus[unit] == "-":
                    if unit and isvalid(partplus[unit - 1]):
                        if not strict:
                            try:
                                if beforedone:
                                    raise ExpressionError("Can not give more than one prefix!")
                                elif begin >= end:
                                    raise ExpressionError("Please give prefix or suffix!")
                            except ExpressionError as Error:
                                print("ExpressionError:", Error)
                                exit()
                        if not afterdone:
                            wordlist = list(part[begin:end]) + wordlist
                            begin = unit

                dotype = partplus[unit]

            begin += 0 if isvalid(partplus[unit]) else 1
            end = begin + 1 if isvalid(partplus[unit]) else unit

    return "".join(wordlist)

we = {
    "do": "~",
    "apple": "^",
    "relevant": "ir-",
    "link": "-s",
    "complicate": "un-d",
    "make": "e>ing",
    "stand": "an=oo",
    "taxman": "a=e",
    "shake": "are |e>ing",
    # "shake": "are e>ing", TOFIX
    "correct": "in-|-ly",
    "correct": "in|-ly",
    "correct": "in-ly",
    "able": "dis|le>ility",
    # "able": "dis-le>ility",
    "favour": "-ite", # E "+ite"
    "mature": "im-ly", # E "im--ly"
    "additional": "^-ly",
    "usual": "un-|-ly",
    "like": "-s", # E "~s"
    "evident": "^-ly", # E "-ly^"
    "agree": "dis-", # E "dis"
    "legal": "il-ly", # E "-ly|il-", "-ly|il"
    # "legal": "il-|-ly", # E "-ly|il-", "-ly|il"
    # "legal": "il|-ly", # E "-ly|il-", "-ly|il"
}

for word, expression in  we.items():
    print(SFBEx(word, expression, False))