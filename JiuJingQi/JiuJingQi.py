import math

class Chess:
    '''
    初始化

    @param {dictionary} config 设置
    '''
    def __init__(self, config):
        # 基本设置

        ## 错误信息
        self._ErrorInfo = {
            1: "坐标格式错误，",
            2: "坐标已被占领，",

            11: "种子格式错误，",
            12: "种子不合法，",

            101: "命令不存在，",
            102: "参数不符合规范，",
        }
        ## 胜利信息
        self._WinInfo = {
            1: "通过率先完成连成一线的任务，",
            2: "通过数量优势碾压了对手，",
            3: "win 指令：",
            4: "对手简直不堪一击，发起了投降，",
        }
        # 信息类别
        self._InfoType = {
            "error": self._ErrorInfo,
            "win": self._WinInfo,
        }
        # 基础命令（带 * 为需要在设置开启指定功能）
        self._Commands = [
            # 模式
            "debug", # *:debug (way) 调试模式 in/1: 进入   out/0: 退出   reverse/-1: 翻转
            # 功能
            "restart", # :restart (way) （以某一方式）重启游戏   1: [默认] 重启 2: 保留当前局面重启
            "quit", # :quit (way) （以某一方式）退出游戏   1: [默认] 保存至历史关闭 2: 不保存至历史关闭
            "mark", # :mark (label) 标记（为某标签「标签默认为当前标签序数，仅可由字母与数字组成，不可重复」）   标记仅可观看，不可进行修改
            "renamemark", # :renamemark <number/label> <label> 重命名某标签
            "marklist", # :marklist 显示标记列表（标记列表默认包含当前局面，标签序号为 0，标签名为 #）
            "clearmark", # :clearmark (number/label) 清理标记列表「默认清空，优先视数字为标签而非序号」   number: 删除指定序号标记（如 1、1,3 和 1-3,5 等语法） label: 删除指定标签名（如 one 和 one,two 等语法）
            "undo", # *:undo (number) 悔棋（几步「默认 1 步，超过轮数则回到第一轮」）
            "redo", # *:redo (number) 重做（几步「默认 1 步，超过轮数回到最新轮，undo 后且未进行任何行棋才可以使用此操作」）
            "history", # *:history 显示历史行棋
            "turn", # *:turn <time> 回到第几轮（去某一轮后若行棋会覆盖后面的历史）
            # 游戏
            "surrender", # :surrender 投降
        ]
        # 调试命令
        self._DebugCommands = [
            # 模式
            "debug", # :debug (way) 调试模式 in/1: 进入   out/0: 退出   reverse/-1: 翻转
            # 功能
            "varlist", # :varlist 获取已知变量 list(filter(lambda m: "__" not in m, dir(self)))
            "check", # :check <var> 查看某一变量
            "run", # :run <code> 运行单行代码
            "goto", # :goto <number/label> 跳转到指定标签
            # 游戏
            "player", # :player (player) 切换为某一玩家「默认为对方」
            "occupy", # :occupy (player) <area> （让某玩家）直接占领某一区域
            "win", # :win (player) (way) （让某玩家通过某种方式「默认为 win 指令」）直接胜利
            "surrender", # :surrender (player) （使某玩家）投降
            "error", # :error <code> 触发某种错误
        ]

        # 导入设置

        self._Config = config # 设置
        self._Signs = (" ", self._Config["first_player_sign"], self._Config["second_player_sign"]) # 标识符
        self._Players = {0: self._Signs[0], 1: self._Signs[1], 2: self._Signs[2]} # 玩家
        self._ReversePlayers = {" ": "0", self._Signs[1]: "1", self._Signs[2]: "2"} # 玩家反映射
        self._Player = self._Config["start_player"] # 当前玩家
        self._Area = self._Config["start_area"] if self._Config["start_area"] else "?" # 当前区域
        self._isDebug = 1 if self._Config["allow_command"]["debug"] and self._Config["start_debug"] else 0 # 调试模式状态
        self._isRepeat = 0

        # 大棋盘

        self._Location = {chr(i): self.__Area() for i in range(ord("A"), ord("J"))} # 区域
        for i in range(ord("A"), ord("J")):
            self._Location[chr(i)]._ReversePlayers = self._ReversePlayers
        self._LocationPosition = {chr(i): self._Location[chr(i)]._Position for i in range(ord("A"), ord("J"))} # 区域情况
        self._AreaOwners = {chr(i): self._Location[chr(i)]._Owner for i in range(ord("A"), ord("J"))} # 区域所属
        self._History = {1: {}, 2: {}} # 行棋记录
        self._Process = "normal" # 进程   normal: 正常游戏   undo: 悔棋模式   mark: 标记模式
        self._Time = 1
        self._Turn = 1

        # 游戏

        self.__Play()

    '''
    游戏
    '''
    def __Play(self):
        # self.__Mode() # 选取游戏模式
        for _ in range(4):
            self.__Render()

    '''
    获取输入

    @return {dictionary} 获取输入状态信息
    '''
    def __Input(self):
        input_content = input(">>> ")
        if input_content == "q":
            exit()
        if input_content.startswith(":"):
            content = input_content[1:].split()
            return self.__Command(content[0], content[1:])
        elif len(input_content) == 2 and (self._Area == "?" or self._Area == input_content[0].upper()) and input_content[0].upper() in [chr(i) for i in range(ord("A"), ord("J"))] and input_content[1] in [str(i) for i in range(1, 10)]:
            if self._Location[input_content[0].upper()]._Owner or (self._Location[input_content[0].upper()]._Position[int(input_content[1])] != " " and not self._isDebug):
                return self.Status__("error", 2)
            self._Location[input_content[0].upper()](self._Players[self._Player], int(input_content[1]))
            self._Area = "?" if self._Location[[chr(i) for i in range(ord("A"), ord("J"))][int(input_content[1]) - 1]]._Owner else [chr(i) for i in range(ord("A"), ord("J"))][int(input_content[1]) - 1]
        elif self._Area != "?" and len(input_content) == 1 and input_content in [str(i) for i in range(1, 10)]:
            if self._Location[self._Area]._Position[int(input_content[0])] != " " and not self._isDebug:
                return self.Status__("error", 2)
            self._Location[self._Area](self._Players[self._Player], int(input_content[0]))
            self._Area = "?" if self._Location[[chr(i) for i in range(ord("A"), ord("J"))][int(input_content[0]) - 1]]._Owner else [chr(i) for i in range(ord("A"), ord("J"))][int(input_content[0]) - 1]
        else:
            return self.Status__("error", 1)
        return self.Status__()

    '''
    命令

    @param {string} command 命令名
    @param {list} params 参数列表
    @return {dictionary} 执行信息
    '''
    def __Command(self, command, params):
        if self._isDebug and (command in self._Commands or command in self._DebugCommands):
            if command == "debug":
                try:
                    return self.__command_debug(*params)
                except:
                    return self.Status__("command_error", content = "未知参数 " + ", ".join(params[1:]) + "，请重新输入！")
            elif command == "restart":
                pass
            elif command == "quit":
                pass
            elif command == "mark":
                pass
            elif command == "marklist":
                pass
            elif command == "clearmark":
                pass
            elif command == "undo":
                pass
            elif command == "redo":
                pass
            elif command == "redo":
                pass
            elif command == "history":
                pass
            elif command == "turn":
                pass
            elif command == "surrender":
                pass
            elif command == "varlist":
                pass
            elif command == "check":
                pass
            elif command == "run":
                pass
            elif command == "goto":
                pass
            elif command == "player":
                pass
            elif command == "occupy":
                pass
            elif command == "win":
                pass
            elif command == "error":
                pass
        elif command in self._Commands and (not command in self._Config["allow_command"] or self._Config["allow_command"][command]):
            if command == "debug":
                try:
                    return self.__command_debug(*params)
                except:
                    return self.Status__("command_error", content = "未知参数 " + ", ".join(params[1:]) + "，请重新输入！")
            elif command == "restart":
                pass
            elif command == "quit":
                pass
            elif command == "mark":
                pass
            elif command == "marklist":
                pass
            elif command == "clearmark":
                pass
            elif command == "undo":
                pass
            elif command == "redo":
                pass
            elif command == "redo":
                pass
            elif command == "history":
                pass
            elif command == "turn":
                pass
            elif command == "surrender":
                pass

    '''
    命令：调试模式

    @param {string}[-1, 1, 0, reverse, in, out] ways 方式
    @return {dictionary} 执行信息
    '''
    def __command_debug(self, way = "-1"):
        if way not in ["-1", "1", "0", "reverse", "in", "out"]:
            return self.Status__("error", 102, way)
        self._isDebug = not self._isDebug if way in ["-1", "reverse"] else "1" if way in ["1", "in"] else 0
        return self.Status__()

    '''
    获取游戏模式

    @return {string}[game, seed] _PlayMode 游戏模式
    '''
    def __Mode(self):
        print("①自定义模式（输入\"seed\"开启）\n②正常模式（输入其他指令即可）")
        self._PlayMode = "seed" if input("请选择游戏模式：").lower() == "seed" else "game"
        if self._PlayMode == "seed":
            get_seed = 0
            while not get_seed:
                info = self.__Unlock(input("seed="))
                get_seed = not info["code"]
                print(info["message"])

    '''
    生成种子

    @param {number}[0 - 2] _Player 当前玩家
    @param {string}[?, A - I] _Area 当前区域
    @param {dictionary} _LocationPosition 棋盘内容
    @return {string} _Seed 种子
    '''
    def __GenSeed(self):
        seed = str(self._Player) + self._Area
        map_way = {**{"000": "0"}, **{self.__Simtern(i - ord("A") + 1): chr(i) for i in range(ord("A"), ord("Z") + 1)}}
        for i in range(ord("A"), ord("J")):
            sequence = ""
            for j in range(1, 10):
                sequence += self._ReversePlayers[self._Location[chr(i)]._Position[j]]
            seed += map_way[sequence[0:3]] + map_way[sequence[3:6]] + map_way[sequence[6:9]]
        self._Seed = seed

    '''
    解锁种子

    @param {string} seed 种子
    @return {number}[0 - 2] _Player 当前玩家
    @return {string}[?, A - Z] _Area 当前区域
    @return {dictionary} _Location 棋盘
    '''
    def __Unlock(self, seed):
        players = ["1", "2"] + (["0"] if self._Config["allow_command"]["debug"] else [])
        areas = [chr(i) for i in range(ord("A"), ord("J"))] + (["?"] if self._Config["allow_command"]["debug"] else [])
        if len(seed) != 29 or seed[0] not in players or seed[1] not in areas:
            return self.Status__("error", 11) # 种子格式错误
        self._Player = int(seed[0])
        self._Area = seed[1]
        map_way = {**{"0": "000"}, **{chr(i): self.__Simtern(i - ord("A") + 1) for i in range(ord("A"), ord("Z") + 1)}}
        for i in range(1, 10):
            for j in range(1, 10):
                self._Location[chr(ord("A") + i)]._Position[j] = self._Players[int((map_way[seed[2 + 3 * i]] + map_way[seed[3 + 3 * i]] + map_way[seed[4 + 3 * i]])[j])]
        return self.Status__()

    '''
    渲染棋盘

    @param {dictionary} _LocationPosition 棋盘内容
    @return {string} _Display 棋盘显示
    '''
    def __Render(self):
        board_roof = "‖‖===========‖‖===========‖‖===========‖‖"
        board_border = "‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖"
        display = board_roof + "\n"
        for i in range(ord("A"), ord("H"), 3):
            for j in range(1, 8, 3):
                display += "‖‖"
                for k in range(i, i + 3):
                    for l in range(j, j + 2):
                        display += " " + self._Location[chr(k)]._Position[l] + " |"
                    display += " " + self._Location[chr(k)]._Position[j + 2] + " ‖‖"
                display += "\n" + board_border + "\n" if j != 7 else ("\n" + board_roof) * 2 + "\n" if j == 7 and i != ord("G") else "\n"
        self._Display = display + board_roof
        # os.system('cls')
        if self._Config["show_seed"]:
            self.__GenSeed()
            print("seed=" + self._Seed)
        print(self._Display)
        print('''  ‖===========‖===========‖===========‖
  ‖ A | B | C ‖ Player: %(player)s ‖ 1 | 2 | 3 ‖
  ‖———|———|———‖ Area: %(area)s   ‖———|———|———‖
  ‖ D | E | F ‖===========‖ 4 | 5 | 6 ‖
  ‖———|———|———‖ Turn: %(turn)-2d  ‖———|———|———‖
  ‖ G | H | I ‖ Time: %(time)-2d  ‖ 7 | 8 | 9 ‖
  ‖===========‖===========‖===========‖''' % {"player": self._Players[self._Player], "area": self._Area, "turn": self._Turn, "time": self._Time})
        input_info = self.__Input()
        while input_info["status"] != "success":
            print(self._ErrorInfo[input_info["code"]] + "请重新输入！")
            input_info = self.__Input()
        self._Time += 1
        if not self._isRepeat:
            if self._Player == 2:
                self._Turn += 1
            self._Player = 3 - self._Player

    '''
    检查游戏是否胜利

    @param {dictionary} _AreaOwners 区域占领情况
    @return {dictionary} 胜利信息
    '''
    def __Check(self):
        for i in range(ord("A"), ord("H"), 3):
            seti = {self._AreaOwners[chr(i)], self._AreaOwners[chr(i) + 1], self._AreaOwners[chr(i) + 2]}
            if len(seti) == 1 and seti != {" "}:
                self._Owner = int(self._ReversePlayers[self._AreaOwners[chr(i)]])
                self.__Check()
                return Chess.Status__("win", 1, self._AreaOwners[i])
        for j in range(ord("A"), ord("D")):
            setj = {self._AreaOwners[chr(j)], self._AreaOwners[chr(j) + 3], self._AreaOwners[chr(j) + 6]}
            if len(setj) == 1 and setj != {" "}:
                self._Owner = int(self._ReversePlayers[self._AreaOwners[chr(j)]])
                self.__Check()
                return Chess.Status__("win", 1, self._AreaOwners[j])
        setk, setl = {self._AreaOwners["A"], self._AreaOwners["E"], self._AreaOwners["I"]}, {self._AreaOwners["C"], self._AreaOwners["E"], self._AreaOwners["G"]}
        if (len(setk) == 1 and setk != {" "}) or (len(setl) == 1 and setl != {" "}):
            self._Owner = int(self._ReversePlayers[self._AreaOwners["E"]])
            self.__Check()
            return Chess.Status__("win", 2, self._AreaOwners["E"])

    '''
    状态信息返回

    @param {string}[error, win] status 状态
    @param {number} code 代码
    @param {anything} content 内容
    @return {dictionary} 信息
    '''
    @classmethod
    def Status__(self, status = "success", code = 0, content = "", scope = "game"):
        return {
            "status": status,
            "code": code,
            "content": content,
            "scope": scope,
        }

    '''
    27 以内三进制

    @param {number}[0 - 26] number 目标数字
    @return {string} 三进制字符串
    '''
    @staticmethod
    def __Simtern(number):
        first = number // 9
        second = (number - first * 9) // 3
        third = number - first * 9 - second * 3
        return str(first) + str(second) + str(third)

    '''
    区域

    @param {number}[0 - 2] player 玩家
    @param {number}[0 - 8] position 占领格
    @return {dictionary} 占领信息
    '''
    class __Area:
        '''
        初始化区域

        @return {number}[0 - 2] _Owner 控制者
        @return {dictionary} _Position 区域格情况
        '''
        def __init__(self):
            self._Owner = 0
            self._Position = {i: " " for i in range(1, 10)}

        '''
        占领区域格并检查区域占领情况

        @param {string} player_sign 玩家标识
        @param {number}[0 - 8] position 占领格位置
        @return {number}[0 - 2] _Owner 控制者
        @return {dictionary} _Position 区域格情况
        @return {dictionary} 占领信息
        '''
        def __call__(self, player_sign, position):
            self._Position[position] = player_sign
            if self._Owner:
                self._Position = {i: player_sign for i in range(1, 10)}
            else:
                for i in range(1, 8, 3):
                    seti = {self._Position[i], self._Position[i + 1], self._Position[i + 2]}
                    if len(seti) == 1 and seti != {" "}:
                        self._Owner = int(self._ReversePlayers[self._Position[i]])
                        self._Position = {i: player_sign for i in range(1, 10)}
                        print(self._Position)
                        return Chess.Status__("win", 1, self._Position[i], "area")
                for j in range(1, 4):
                    setj = {self._Position[j], self._Position[j + 3], self._Position[j + 6]}
                    if len(setj) == 1 and setj != {" "}:
                        self._Owner = int(self._ReversePlayers[self._Position[j]])
                        self._Position = {i: player_sign for i in range(1, 10)}
                        return Chess.Status__("win", 1, self._Position[j], "area")
                setk, setl = {self._Position[1], self._Position[5], self._Position[9]}, {self._Position[3], self._Position[5], self._Position[7]}
                if (len(setk) == 1 and setk != {" "}) or (len(setl) == 1 and setl != {" "}):
                    self._Owner = int(self._ReversePlayers[self._Position[5]])
                    self._Position = {i: player_sign for i in range(1, 10)}
                    return Chess.Status__("win", 2, self._Position[5], "area")

config = {
    "first_player_sign": "X",
    "second_player_sign": "O",
    "start_player": 1,
    "start_area": "?",
    "show_seed": 1,
    "start_debug": 1,
    "allow_command": {
        "debug": 1,
        "undo": 1,
        "redo": 1,
        "history": 1,
        "turn": 1,
    },
}

JiuJingQi = Chess(config)