# seed=0?0BG0TP0ROWDBPTPWLR000WF0000
# ‖‖===========‖‖===========‖‖===========‖‖
# ‖‖   |   |   ‖‖   |   |   ‖‖   |   |   ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   |   | O ‖‖ O |   | O ‖‖ O |   |   ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   | O | X ‖‖ X | O | X ‖‖ X | O |   ‖‖
# ‖‖===========‖‖===========‖‖===========‖‖
# ‖‖===========‖‖===========‖‖===========‖‖
# ‖‖ O | X | O ‖‖ X | O | X ‖‖ O | X | O ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   | X | X ‖‖ O |   | O ‖‖ X | X |   ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   |   | O ‖‖ X | O | X ‖‖ O |   |   ‖‖
# ‖‖===========‖‖===========‖‖===========‖‖
# ‖‖===========‖‖===========‖‖===========‖‖
# ‖‖   |   |   ‖‖ O | X | O ‖‖   |   |   ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   |   |   ‖‖   | O |   ‖‖   |   |   ‖‖
# ‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
# ‖‖   |   |   ‖‖   |   |   ‖‖   |   |   ‖‖
# ‖‖===========‖‖===========‖‖===========‖‖

# 计划
## 增加「?」，可用于清除
## 增加游戏配置与历史记录、胜率等查询
## 增加指令
### occupy: 可输入字母占领某个「井」
### win: 直接取得游戏胜利
#### win(sb.): 使指定玩家直接获得游戏胜利
### surrender: 投降
#### surrender(sb.): 使指定玩家直接投降
### player: 切换玩家（包括「?」）
### restart: 重启游戏
## 增加模式
### setting: 进入设置
#### clear: 清除历史记录等
#### reset: 重置设置
### information: 进入历史记录查询模式

# 引用区
import copy
import os

# 初始化设置区
## 初始化设置

# 内部定义区
signs = (" ", "X", "O")
Bboard = [chr(i) for i in range(ord("A"), ord("J"))]
Sboard = [i for i in range(1, 10)]
players = {0: signs[0], 1: signs[1], 2: signs[2]}
historys = {signs[1]: {}, signs[2]: {}}
Bhistorys = {signs[1]: {}, signs[2]: {}}
Ohistorys = {signs[1]: {}, signs[2]: {}}

# 内置函数区
## 初始化胜利点
def initown():
    temp = {}
    for i in range(1, 10):
        temp[i] = " "
    return temp

## 初始化棋局
def initloc(set):
    for i in range(ord("A"), ord("J")):
        set[chr(i)] = {}
        for j in range(1, 10):
            set[chr(i)][j] = players[0]
    return set

## 输出棋盘
def chessboard(set):
    border1 = "‖‖===========‖‖===========‖‖===========‖‖"
    border2 = "‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖"
    result = (border1 + "\n")
    for i in range(ord("A"), ord("H"), 3):
        for j in range(1, 8, 3):
            result += "‖‖"
            for k in range(i, i + 3):
                for l in range(j, j + 2):
                    result += " " + set[chr(k)][l] + " |"
                result += " " + set[chr(k)][j + 2] + " ‖‖"
            if j != 7:
                result += "\n" + border2 + "\n"
            elif j == 7 and i != ord("G"):
                result += ("\n" + border1)*2 + "\n"
            else:
                result += "\n"
    result += border1
    return result

## 输入坐标
def inp(player, Bsign):
    if Bsign == "?":
        return input("请输入 " + players[player] + " 的下一步坐标：").upper()
    else:
        return input("请输入 " + players[player] + " 在 " + Bsign + " 区的下一步坐标：").upper()

## 获取坐标
def get(str, pos, opt, owner):
    if len(str) > 2:
        if str == "BUG":
            return "debug"
        elif opt == "debug" and str == "REPEAT":
            return "repeat"
        elif str == "OUT":
            return "out"
        elif str == "UNDO":
            return "undo1"
        elif str == "REDO":
            return "redo1"
        elif str[0:4] == "UNDO":
            return str.lower()
        elif str[0:4] == "REDO":
            return str.lower()
    elif len(str) == 1 and pos != "?":
        Bsign = pos
        Ssign = int(str)
    elif len(str) == 2:
        Bsign = str[0]
        Ssign = int(str[1])
    else:
        return "wrong1"
    if opt == "debug":
        return {"Bsign": Bsign, "Ssign": Ssign}
    if pos != "?":
        if owner[ord(pos) - ord("A") + 1] != " " and owner[ord(Bsign) - ord("A") + 1] == " ":
            return {"Bsign": Bsign, "Ssign": Ssign}
    if (len(str) == 2 and (pos == "?" or pos == Bsign)) or (len(str) == 1 and pos != "?"):
        if Bsign in Bboard and int(Ssign) in Sboard:
            return {"Bsign": Bsign, "Ssign": Ssign}
        else:
            return "wrong2" # 溢出错误
    else:
        return "wrong1" # 格式错误

## 获取占有情况
def getin(set, pos):
    return set[pos["Bsign"]][pos["Ssign"]]

## 行棋合理性判断
def mod(set, pos, owner):
    if owner[ord(pos["Bsign"]) - ord("A") + 1] == " " and getin(set, pos) == " ":
        return ""
    else:
        return "wrong3" # 无效行棋

## 值->键
def vvalue(dic, value):
    return list(dic.keys())[list(dic.values()).index(value)]

## 元素数量
def num(set, str):
    temp = 0
    for i in set:
        if i == str:
            temp += 1
    return temp

## 判断是否胜利
def winever(set):
    nums = {}
    result = "nowin"
    for key, value in players.items():
        nums[key] = num(set.values(), value)
    if max(nums.values()) >= 5 and nums[0] == 0:
        result =  ["win2", vvalue(nums, max(nums.values())), max(nums.values())] # 胜利 2
    for i in range(1, 4):
        if set[i] == set[i + 3] == set[i + 6] != signs[0]:
            result =  ["win1", vvalue(players, set[i]), max(nums.values())] # 胜利 1
    for j in range(1, 8, 3):
        if set[j] == set[j + 1] == set[j + 2] != signs[0]:
            result =  ["win1", vvalue(players, set[j]), max(nums.values())]
    if set[1] == set[5] == set[9] != signs[0] or set[3] == set[5] == set[7] != signs[0]:
        result = ["win1", vvalue(players, set[5]), max(nums.values())]
    return result

## 错误信息
def wrong(inf):
    wrongs = {"wrong1": "坐标格式错误！", "wrong2": "坐标不存在！", "wrong3": "无效行棋！", "wrong4": "种子格式错误！", "wrong5": "种子不合法！"}
    return wrongs[inf] + "请重新输入！"

## 胜利信息
def win(inf):
    wins = {"win1": "通过率先完成连成一线的任务，", "win2": "通过数量优势碾压了对手，", "win3": "win 指令：","win4": "对手简直不堪一击，发起了投降，"}
    return wins[inf]

## 游戏模式
def mode(inf):
    if inf.lower() == "seed":
        return "seed"
    else:
        return "game"

## 简单三进制（仅支持 27 以内）
def simtern(num):
    a = num // 9
    b = (num - a*9) // 3
    c = num - a*9 - b*3
    return str(a) + str(b) + str(c)

## 字符串替换
def streplace(str, restr, start, end):
    result = str[:start] + restr + str[end:]
    return result

## 种子
def seed(set, player, sign):
    temp = {" ": "0", signs[1]: "1", signs[2]: "2"}
    seed = str(player) + sign
    for i in range(ord("A"), ord("J")):
        for j in range(1, 10):
            seed += temp[set[chr(i)][j]]
    tempset = {"000": "0"}
    for i in range(ord("A"), ord("Z") + 1):
        tempset[simtern(i - ord("A") + 1)] = chr(i)
    for i in range(26, -1, -1):
        seed = streplace(seed, tempset[seed[3*i + 2:3*i + 5]], 3*i + 2, 3*i + 5)
    return seed

## 解码
def unlock(seed):
    if len(seed) != 29:
        return "wrong4" # 种子格式错误
    temp = {"0": " ", "1": signs[1], "2": signs[2]}
    player = int(seed[0]) if bool(seed[0]) else -1
    sign = seed[1]
    set = {}
    tempset = {"0": "000"}
    owner = initown()
    for i in range(ord("A"), ord("Z") + 1):
        tempset[chr(i)] = simtern(i - ord("A") + 1)
    for i in range(26, -1, -1):
        seed = streplace(seed, tempset[seed[i + 2]], i + 2, i + 3)
    for i in range(ord("A"), ord("J")):
        set[chr(i)] = {}
        for j in range(1, 10):
            set[chr(i)][j] = temp[seed[(i - ord("A"))*9 + j + 1]]
    for i in range(ord("A"), ord("J")):
        if winever(set[chr(i)]) != "nowin" and winever(set[chr(i)])[2] != 9:
            return "wrong5" # 种子不合法
        elif winever(set[chr(i)]) != "nowin":
            owner[i - ord("A") + 1] = players[winever(set[chr(i)])[1]]
    if winever(owner) != "nowin" or (sign != "?" and owner[ord(sign) - ord("A") + 1] != " "):
        return "wrong5"
    return [player, sign, set, owner]

## 主程序
def chess():
    ### 游戏定义区
    istrue = 0
    his = 0
    player = 1
    step = 1
    winner = 0
    Bsign = "?"
    setting = 1
    sed = 0
    steplayer = 0
    locations = initloc({})
    owner = initown()
    os.system('cls')
    print("①自定义模式（输入\"seed\"开启）\n②正常模式（输入其他指令即可）")
    modes = mode(input("请选择游戏模式："))
    if modes == "seed":
        while sed == 0:
            seeds = input("seed=")
            if isinstance(unlock(seeds), str):
                print(wrong(unlock(seeds)))
            else:
                player = unlock(seeds)[0]
                Bsign = unlock(seeds)[1]
                locations = unlock(seeds)[2]
                owner = unlock(seeds)[3]
                sed = 1
    os.system('cls')
    print("seed=" + seed(locations, player, Bsign))
    print(chessboard(locations))
    while winner == 0:
        print("现在为第 " + str(step) + " 轮，轮到 " + players[player] + " 行棋！")
        print('''  ‖===========‖===========‖===========‖
  ‖ A | B | C ‖           ‖ 1 | 2 | 3 ‖
  ‖———|———|———‖           ‖———|———|———‖
  ‖ D | E | F ‖           ‖ 4 | 5 | 6 ‖
  ‖———|———|———‖           ‖———|———|———‖
  ‖ G | H | I ‖           ‖ 7 | 8 | 9 ‖
  ‖===========‖===========‖===========‖''')
        if setting == 1 and his == 0:
            steplayer = abs(player - 2) + 1
        else:
            steplayer = player
        if his == 0:
            historys[players[player]][step] = copy.deepcopy(locations)
            Ohistorys[players[player]][step] = copy.deepcopy(owner)
            Bhistorys[players[player]][step] = Bsign
        his = 0
        while istrue == 0:
            instr = inp(player, Bsign)
            loc = get(instr, Bsign, 0, owner)
            if setting == 1 and (loc == "wrong1" or loc == "wrong2"):
                print(wrong(loc))
            elif loc == "debug":
                print("进入临时 debug 模式！")
                instr = inp(player, Bsign)
                loc = get(instr, Bsign, "debug", owner)
                if loc == "repeat":
                    print("进入 repeat 模式！")
                    instr = inp(player, Bsign)
                    loc = get(instr, Bsign, "debug", owner)
                    steplayer = player
                    setting = 0
                istrue = 1
            elif loc == "out": # 进入 repeat 模式不可立刻 out
                setting = 1
            elif setting == 0:
                loc = get(instr, Bsign, "debug", owner)
                istrue = 1
            elif isinstance(loc, str) and loc[0:4] == "undo":
                if step - int(loc[4:]) <= 1:
                    step = 1
                else:
                    step -= int(loc[4:])
                his = 1
                istrue = 1
            elif isinstance(loc, str) and loc[0:4] == "redo":
                if step + int(loc[4:]) >= len(historys[players[player]]):
                    step = len(historys[players[player]])
                else:
                    step += int(loc[4:])
                his = 1
                istrue = 1
            else:
                if mod(locations, loc, owner) == "":
                    istrue = 1
                else:
                    print(wrong(mod(locations, loc, owner)))
        if his == 0:
            locations[loc["Bsign"]][loc["Ssign"]] = players[player]
        for i in range(ord("A"), ord("J")):
            if winever(locations[chr(i)]) != "nowin":
                if owner[i - ord("A") + 1] == " ":
                    print(win(winever(locations[chr(i)])[0]) + players[winever(locations[chr(i)])[1]] + " 完成了对 " + chr(i) + " 区的占领！")
                for j in range(1, 10):
                    locations[chr(i)][j] = players[winever(locations[chr(i)])[1]]
                owner[i - ord("A") + 1] = players[winever(locations[chr(i)])[1]]
        if his == 1:
            locations = historys[players[player]][step]
            owner = Ohistorys[players[player]][step]
            Bsign = Bhistorys[players[player]][step]
        else:
            Bsign = chr(ord("A") + loc["Ssign"] - 1)
        if Bsign == "?" or owner[ord(Bsign) - ord("A") + 1] != " ":
            Bsign = "?"
        os.system('cls')
        print("seed=" + seed(locations, steplayer, Bsign))
        print(chessboard(locations))
        if winever(owner) != "nowin":
            print(win(winever(owner)[0]) + players[winever(owner)[1]] + " 获得了游戏的胜利！")
            winner = winever(owner)[1]
        if his == 0:
            if step < len(historys[players[player]]):
                for i in range(step + 1, len(historys[players[player]]) + 1):
                    del historys[players[player]][i]
                    del Bhistorys[players[player]][i]
                    del Ohistorys[players[player]][i]
        if setting == 1 and his == 0:
            if player == 2:
                step += 1
            player = abs(player - 2) + 1
            # player = int(not bool(player - 1)) + 1
            # set[(num + 1)*abs(num // (len(set) - 1) - 1)]
            # 取列表 set 第 num 个元素的下一个元素，若 num 已为最后一个元素返回首个元素
        istrue = 0

# 运行区
chess()