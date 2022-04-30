class Chess:
    '''
    初始化

    @param {dictionary} config 设置
    '''
    def __init__(self, config):
        # 基本设置

        ## 错误信息
        self._ErrorInfo = {
            1: "坐标错误！",

            11: "种子格式错误！",
            12: "种子不合法！",
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
            "debug", # *:debug (way) 调试模式 in/1: 进入   out/0: 退出
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
            "debug", # :debug (way) 调试模式 in/1: 进入   out/0: 退出
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
        self._Area = self._Config["start_place"] if self._Config["start_place"] else "?" # 当前区域
        self._isDebug = 1 if self._Config["allow_debug"] and self._Config["start_debug"] else 0 # 调试模式状态

        # 大棋盘

        self._Location = {chr(i): self.__Area() for i in range(ord("A"), ord("J"))} # 区域
        for i in range(ord("A"), ord("J")):
            self._Location[chr(i)]._Players = self._Players
            self._Location[chr(i)]._ReversePlayers = self._ReversePlayers
        self._LocationPosition = {chr(i): self._Location[chr(i)]._Position for i in range(ord("A"), ord("J"))} # 区域情况
        self._AreaOwners = {chr(i): self._Location[chr(i)]._Owner for i in range(ord("A"), ord("J"))} # 区域所属
        self._History = {1: {}, 2: {}} # 行棋记录
        self._Process = "normal" # 进程   normal: 正常游戏   undo: 悔棋模式   mark: 标记模式

        # 游戏

        self.__Play()

    '''
    游戏
    '''
    def __Play(self):
        # self.__Mode() # 选取游戏模式
        self.__Render()

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
    信息状态返回

    @param {string}[error, win] status 状态
    @param {number} code 代码
    @param {anything} content 内容
    @return {dictionary} 信息
    '''
    @classmethod
    def Status__(self, status = "success", code = 0, content = ""):
        return {
            "status": status,
            "code": code,
            "content": content
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
            for j in range(9):
                sequence += self._ReversePlayers[self._LocationPosition[chr(i)][j]]
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
        players = ["1", "2"] + (["0"] if self._Config["allow_debug"] else [])
        areas = [chr(i) for i in range(ord("A"), ord("J"))] + (["?"] if self._Config["allow_debug"] else [])
        if len(seed) != 29 or seed[0] not in players or seed[1] not in areas:
            return self.Status__("error", 11) # 种子格式错误
        self._Player = int(seed[0])
        self._Area = seed[1]
        map_way = {**{"0": "000"}, **{chr(i): self.__Simtern(i - ord("A") + 1) for i in range(ord("A"), ord("Z") + 1)}}
        for i in range(9):
            for j in range(9):
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
            for j in range(0, 7, 3):
                display += "‖‖"
                for k in range(i, i + 3):
                    for l in range(j, j + 2):
                        display += " " + self._LocationPosition[chr(k)][l] + " |"
                    display += " " + self._LocationPosition[chr(k)][j + 2] + " ‖‖"
                display += "\n" + board_border + "\n" if j != 6 else ("\n" + board_roof) * 2 + "\n" if j == 6 and i != ord("G") else "\n"
        self._Display = display + board_roof
        # os.system('cls')
        if self._Config["show_seed"]:
            self.__GenSeed()
            print("seed=" + self._Seed)
        print(self._Display)

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
            self._Position = {i: " " for i in range(9)}

        '''
        占领区域格

        @param {number}[0 - 2] player 玩家
        @param {number}[0 - 8] position 占领格
        @return {dictionary} 占领信息
        '''
        def __call__(self, player, position):
            self._Position[position] = self._Players[player]
            return self.__Check()

        '''
        检查区域占领情况

        @param {number}[0 - 2] _Owner 控制者
        @param {dictionary} _Position 区域格情况
        @return {dictionary} 占领信息
        '''
        def __Check(self):
            if self._Owner:
                self._Position = {i: self._Players[self._Owner] for i in range(9)}
            else:
                for i in range(0, 7, 3):
                    seti = {self._Position[i], self._Position[i + 1], self._Position[i + 2]}
                    if len(seti) == 1 and seti != {" "}:
                        self._Owner = int(self._ReversePlayers[self._Position[i]])
                        self.__Check()
                        return Chess.Status__("win", 1, self._Position[i])
                for j in range(3):
                    setj = {self._Position[j], self._Position[j + 3], self._Position[j + 6]}
                    if len(setj) == 1 and setj != {" "}:
                        self._Owner = int(self._ReversePlayers[self._Position[j]])
                        self.__Check()
                        return Chess.Status__("win", 1, self._Position[j])
                setk, setl = {self._Position[0], self._Position[4], self._Position[8]}, {self._Position[2], self._Position[4], self._Position[6]}
                if (len(setk) == 1 and setk != {" "}) or (len(setl) == 1 and setl != {" "}):
                    self._Owner = int(self._ReversePlayers[self._Position[4]])
                    self.__Check()
                    return Chess.Status__("win", 2, self._Position[4])

config = {
    "first_player_sign": "X",
    "second_player_sign": "O",
    "start_player": 1,
    "start_place": "",
    "show_seed": 1,
    "allow_debug": 1,
    "start_debug": 1,
}

JiuJingQi = Chess(config)