from re import sub, search
from os import listdir, mkdir
from os.path import exists, dirname, basename, join, split, abspath
from shutil import copy, rmtree
from datetime import datetime

def E2C(string):
    """
    Adapted from https://blog.csdn.net/nanbei2463776506/article/details/82967140
    """
    E_pun = u',;()'
    C_pun = u'，；（）'
    table = {ord(f): ord(t) for f, t in zip(E_pun,C_pun)}
    return string.translate(table)

def Format(txt):
    txt = txt.lower()
    txt = E2C(txt)
    txt = sub(r" +\n", r"\n", txt)
    txt = sub(r"(?<=[\u4e00-\u9fa5])\.{2}|\.{2}(?=[\u4e00-\u9fa5])", r"……", txt)
    txt = sub(r" ?\.{3} ?", r" ... ", txt)
    txt = sub(r"·|・", r".", txt)
    txt = sub(r"_{2,}", r"", txt)
    txt = txt.replace("!", "'")
    txt = txt.replace("a^j", "adj")
    txt = txt.replace("a<j", "adj")
    txt = txt.replace(" fbr ", " for ")
    return txt.strip()

def Select(dir, tempdir):
    files = listdir(dir)
    basfiles, extfiles, phrfiles = [], [], []
    for file in files:
        copy(join(dir, file), tempdir)
        if file[1] in "12":
            basfiles += [file]
        elif file[1] == "e":
            extfiles += [file]
        elif file[1] == "p":
            phrfiles += [file]
    return [basfiles, extfiles, phrfiles]

def EC(list):
    es, cs = [], []
    for file in list:
        if file[0] == "e":
            es += [file]
        elif file[0] == "c":
            cs += [file]
    return [es, cs]

def Basic(e, c):
    with open(e, encoding = "UTF-8-sig") as engs:
        words = []
        for eng in engs.readlines():
            words += [eng.strip('\n')]
    with open(c, encoding = "UTF-8-sig") as chis:
        definitions = []
        phonetics = []
        for chi in chis.readlines():
            defre = search(r"^([^a-z]+)(?=\s?(?:v|n|prep|pron|conj|adj|adv|num|int|phr)\.)", chi.strip('\n'))
            phore = search(r"(?<![a-z])(v|n|prep|pron|conj|adj|adv|num|int|phr)\.", chi.strip('\n'))
            definitions += [defre.group(1)]
            phonetics += [phore.group(1)]
    if not (len(words) == len(definitions) == len(phonetics)):
        print("Basic-Words-File Error! Please format relative files manually.")
        global Error
        Error = True
        return 
    mixs = list(zip(words, definitions, phonetics))
    with open("G:/Assets/Tool/Python/Words2Anki/Data/ECres/Basic.txt", "a+", encoding = "UTF-8") as file:
        for i in range(0, len(words)):
            file.write("\t".join(mixs[i]) + "\n")

def Extra(e, c):
    with open(e, encoding = "UTF-8-sig") as engs:
        words = []
        phonetics = []
        for eng in engs.readlines():
            worre = search(r"^([\w -]+)(?=\s(?:v|n|prep|pron|conj|adj|adv|num|int|phr)\.)", eng.strip('\n'))
            phore = search(r"(?<![a-z])(v|n|prep|pron|conj|adj|adv|num|int|phr)\.", eng.strip('\n'))
            words += [worre.group(1)]
            phonetics += [phore.group(1)]
    with open(c, encoding = "UTF-8-sig") as chis:
        definitions = []
        for chi in chis.readlines():
            definitions += [chi.strip('\n')]
    if not (len(words) == len(definitions) == len(phonetics)):
        print("Extra-Words-File Error! Please format relative files manually.")
        global Error
        Error = True
        return 
    mixs = list(zip(words, definitions, phonetics))
    with open("G:/Assets/Tool/Python/Words2Anki/Data/ECres/Extra.txt", "a+", encoding = "UTF-8") as file:
        for i in range(0, len(words)):
            file.write("\t".join(mixs[i]) + "\n")

def Phrase(e, c):
    with open(e, encoding = "UTF-8-sig") as engs:
        words = []
        for eng in engs.readlines():
            words += [eng.strip('\n')]
    with open(c, encoding = "UTF-8-sig") as chis:
        definitions = []
        for chi in chis.readlines():
            definitions += [chi.strip('\n')]
    if len(words) != len(definitions):
        print("Phrases-File Error! Please format relative files manually.")
        global Error
        Error = True
        return 
    with open("G:/Assets/Tool/Python/Words2Anki/Data/ECres/Phrases.txt", "a+", encoding = "UTF-8") as file:
        for i in range(0, len(words)):
            file.write(words[i] + "\t" + definitions[i] + "\tphr\n")

def Do(target, temptarget, typefile, function):
    ecs = EC(typefile)
    for i in range(2):
        for f in ecs[i]:
            with open(join(temptarget, f), "w+", encoding = "UTF-8-sig") as tfl:
                with open(join(target, f), encoding = "UTF-8-sig") as fl:
                    tfl.write(Format(fl.read()))
    for m, n in zip(ecs[0], ecs[1]):
        function(join(temptarget, m), join(temptarget, n))

def Clear(dir, img = False, pdf = False, txt = False, res = False):
    dirs = ["ECimg", "ECpdf", "ECtxt", "ECres"]
    if img:
        rmtree(join(dir, dirs[0]))
        mkdir(join(dir, dirs[0]))
    if pdf:
        rmtree(join(dir, dirs[1]))
        mkdir(join(dir, dirs[1]))
    if txt:
        rmtree(join(dir, dirs[2]))
        mkdir(join(dir, dirs[2]))
    if res:
        rmtree(join(dir, dirs[3]))
        mkdir(join(dir, dirs[3]))

def CopyDir(source, target):
    mkdir(join(target, basename(source)))
    for file in listdir(source):
        copy(join(source, file), join(target, basename(source)))

def History(dir):
    if exists(join(dir, "EChistory", datetime.now().strftime("%Y-%m-%d"))):
        print("The specific history is existent! Please use \"ClearHistory\" function if you prefer this history.")
        return
    mkdir(join(dir, "EChistory", datetime.now().strftime("%Y-%m-%d")))
    CopyDir(join(dir, "ECimg"), join(dir, "EChistory", datetime.now().strftime("%Y-%m-%d")))
    CopyDir(join(dir, "ECpdf"), join(dir, "EChistory", datetime.now().strftime("%Y-%m-%d")))
    CopyDir(join(dir, "ECres"), join(dir, "EChistory", datetime.now().strftime("%Y-%m-%d")))

def ClearHistory(dir = join(split(abspath(__file__))[0], "Data", "EChistory"), target = "", do = False, all = False):
    if do:
        if all:
            rmtree(dir)
            mkdir(dir)
        else:
            rmtree(join(dir, target))

def Main(cache = False, clear = False, beforeclear = False, history = True):
    dir = join(split(abspath(__file__))[0], "Data")
    target = join(dir, "ECtxt")
    if beforeclear:
        Clear(dir, res = True)
        rmtree(join(dir, "ECtemp"))
        mkdir(join(dir, "ECtemp"))
    [basfiles, extfiles, phrfiles] = Select(target, join(dir, "ECtemp"))
    files = [basfiles, extfiles, phrfiles]
    funcs = [Basic, Extra, Phrase]
    for i in range(3):
        Do(target, join(dir, "ECtemp"), files[i], funcs[i])
    if not cache:
        rmtree(join(dir, "ECtemp"))
        mkdir(join(dir, "ECtemp"))
    if clear:
        Clear(dir, img = False, pdf = False, txt = True, res = False)
    if not Error and history:
        History(dir)

Error = False
ClearHistory(target = "", do = False, all = False)
Main(cache = False, clear = False, beforeclear = True, history = True)

# 使用方法
##1 将单词表分区截图
##2 使用 ABBYY 同名自动化任务
##3 运行此程序（若出错则手动修正）
##4 进入 ECres 获取 txt
##5 导入 Anki
# 单词表分区
## Basic
### e?
### c?
## Extra
### ee?
### ce?
## Phrase
### ep?
### cp?