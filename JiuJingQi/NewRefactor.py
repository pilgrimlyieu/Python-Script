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

import random

class Jing: # {{{1 Jing
    """A Jing is a sub-board(3x3) in JiuJingQi

    Arguments:
        init (dict, optional): Configures for the Jing. Defaults to {"owner": None, "board": None}.

    Attributes:
        _Owner      (int):  The owner of the Jing. 0 for no owner, 1 for player 1, 2 for player 2.
        _finalBoard (list): The final board of the Jing if there's an owner. 0 for no owner, 1 for player 1, 2 for player 2.
        _subBoard   (list): The current board of the Jing. 0 for no owner, 1 for player 1, 2 for player 2.
        _Captured   (list): The number of captured positions in the Jing for each player.

    Methods:
        _HaveCaptured: Returns the number of captured positions in the Jing.
        _Capture:      Captures a position in the Jing.
        _CheckValid:   Checks if the position to be captured is valid.
        _CheckOwner:   Checks if the Jing has an owner.
        _Occupy:       Sets the owner of the Jing.
    """
    def __init__(self, init: dict = {"owner": None, "board": None}):
        self._Owner = 0 if init["owner"] is None else init["owner"]
        self._subBoard = [[0 for i in range(3)] for j in range(3)] if init["board"] is None else init["board"]
        self._finalBoard = self._subBoard
        self._Captured = self._HaveCaptured()
        self._CheckOwner()

    def _HaveCaptured(self):
        occupied = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                    occupied[self._subBoard[i][j]] += 1
        return occupied

    def _Capture(self, player: int, position: tuple):
        if self._CheckValid(position):
            self._subBoard[position[0]][position[1]] = player
            if not self._CheckOwner():
                self._finalBoard = self._subBoard
            self._Captured[player] += 1
            self._Captured[0] -= 1
            return 1
        else:
            # TODO: Raise an error
            return 0

    def _CheckValid(self, position: tuple):
        return self._Owner == 0 and self._subBoard[position[0]][position[1]] == 0

    def _CheckOwner(self):
        for i in range(3):
            row_result = self._subBoard[i][0] & self._subBoard[i][1] & self._subBoard[i][2]
            col_result = self._subBoard[0][i] & self._subBoard[1][i] & self._subBoard[2][i]
            if self._Occupy(row_result) or self._Occupy(col_result):
                return 1
        diag_result_1 = self._subBoard[0][0] & self._subBoard[1][1] & self._subBoard[2][2]
        diag_result_2 = self._subBoard[0][2] & self._subBoard[1][1] & self._subBoard[2][0]
        if self._Occupy(diag_result_1) or self._Occupy(diag_result_2):
            return 1
        if self._Captured[0] == 0:
            self._Occupy(1 if self._Captured[1] > self._Captured[2] else 2)
            return 1
        return 0

    def _Occupy(self, player: int):
        if player == 0:
            return 0
        self._Owner = player
        self._finalBoard = self._subBoard
        self._subBoard = [[player for i in range(3)] for j in range(3)]
        return 1
# }}}1

class JiuJingQi: # {{{1 JiuJingQi
    """JiuJingQi is a board game.

    Arguments:
        config (dict, optional): Configures for the game. Defaults to {}.

    Constants:
        DEFAULT_SIGNS (tuple): The default signs for the players.

    Attributes:
        _Config  (dict):  The configuration of the game.
        _Signs   (tuple): The signs for the players.
        _Players (list):  The players.
        _Board   (dict):  The board of the game.
        _History (list):  The history of the game.
        _Player  (int):   The current player.
        _Time    (int):   The current time.
        _Turn    (int):   The current turn.
        _Area    (str):   The current area.

    Methods:
        _GenerateSeed: Generates a seed for the current board.
        _UnpackSeed:   Unpacks a seed to the current board.
        _Ord2Jing:     Converts an order to a Jing.
        _CheckWinner:  Checks if there's a winner.
        _PrintBoard:   Prints the board.
    """
    def __init__(self, config: dict = {}): # {{{1 JiuJingQi Init
        self.DEFAULT_SIGNS = (" ", "X", "O")

        self._Config = config
        self._Signs = self._Config["signs"] or self.DEFAULT_SIGNS
        self._Players = [sign for sign in self._Signs]
        self._Board = {chr(i): Jing({
            "owner": None,
            # "board": [[random.randint(0, 2) for i in range(3)] for j in range(3)]  # Random board to test
            "board": None,
            }) for i in range(ord("A"), ord("J"))}
        self._History = []
        self._Player = 1 if self._Config["first_player" ]is None else self._Config["first_player"]
        self._Turn = 1
        self._Jing = "?" if self._Config["first_area"] is None else self._Config["first_area"]
    # }}}1

    def _GenerateSeed(self): # {{{1 GenerateSeed
        seed = str(self._Player) + self._Jing
        seed_map = {"000": "0", "001": "A", "002": "B", "010": "C", "011": "D", "012": "E", "020": "F", "021": "G", "022": "H", "100": "I", "101": "J", "102": "K", "110": "L", "111": "M", "112": "N", "120": "O", "121": "P", "122": "Q", "200": "R", "201": "S", "202": "T", "210": "U", "211": "V", "212": "W", "220": "X", "221": "Y", "222": "Z"}
        for i in range(ord("A"), ord("J")):
            sequence = ""
            for j in range(3):
                for k in range(3):
                    sequence += str(self._Board[chr(i)]._subBoard[j][k])
            seed += seed_map[sequence[0:3]] + seed_map[sequence[3:6]] + seed_map[sequence[6:9]]
        return seed
    # }}}1

    def _UnpackSeed(self, seed: str): # {{{1 UnpackSeed
        try:
            if len(seed) != 29:
                raise Exception("Invalid seed length")
            self._Player = int(seed[0])
            self._Jing = seed[1]
            seed_map = {"0": "000", "A": "001", "B": "002", "C": "010", "D": "011", "E": "012", "F": "020", "G": "021", "H": "022", "I": "100", "J": "101", "K": "102", "L": "110", "M": "111", "N": "112", "O": "120", "P": "121", "Q": "122", "R": "200", "S": "201", "T": "202", "U": "210", "V": "211", "W": "212", "X": "220", "Y": "221", "Z": "222"}
            for i in range(2, 29):
                row_map = seed_map[seed[i]]
                for j in range(3):
                    self._Board[self._Ord2Jing(i // 3)]._subBoard[(i - 2) % 3][j] = int(row_map[j])
        except:
            pass # TODO: Raise an error
    # }}}1

    def _Ord2Jing(self, order: int): # {{{1 Order2Jing
        return chr(ord("A") + order)
    # }}}1

    def _CheckWinner(self): # {{{1 CheckWinner
        for i in range(3):
            row_result = self._Board[self._Ord2Jing(i * 3)]._Owner & self._Board[self._Ord2Jing(i * 3 + 1)]._Owner & self._Board[self._Ord2Jing(i * 3 + 2)]._Owner
            col_result = self._Board[self._Ord2Jing(i)]._Owner & self._Board[self._Ord2Jing(i + 3)]._Owner & self._Board[self._Ord2Jing(i + 6)]._Owner
            if row_result == 1 or col_result == 1:
                return 1
            elif row_result == 2 or col_result == 2:
                return 2
        diag_result_1 = self._Board["A"]._Owner & self._Board["E"]._Owner & self._Board["I"]._Owner
        diag_result_2 = self._Board["C"]._Owner & self._Board["E"]._Owner & self._Board["G"]._Owner
        if diag_result_1 == 1 or diag_result_2 == 1:
            return 1
        elif diag_result_1 == 2 or diag_result_2 == 2:
            return 2
        return 0
    # }}}1

    def _PrintBoard(self): # {{{1 PrintBoard
        output = \
    '''seed={seed:s}
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {B[0][0][0]} | {B[0][0][1]} | {B[0][0][2]} ‖‖ {B[1][0][0]} | {B[1][0][1]} | {B[1][0][2]} ‖‖ {B[2][0][0]} | {B[2][0][1]} | {B[2][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[0][1][0]} | {B[0][1][1]} | {B[0][1][2]} ‖‖ {B[1][1][0]} | {B[1][1][1]} | {B[1][1][2]} ‖‖ {B[2][1][0]} | {B[2][1][1]} | {B[2][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[0][2][0]} | {B[0][2][1]} | {B[0][2][2]} ‖‖ {B[1][2][0]} | {B[1][2][1]} | {B[1][2][2]} ‖‖ {B[2][2][0]} | {B[2][2][1]} | {B[2][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {B[3][0][0]} | {B[3][0][1]} | {B[3][0][2]} ‖‖ {B[4][0][0]} | {B[4][0][1]} | {B[4][0][2]} ‖‖ {B[5][0][0]} | {B[5][0][1]} | {B[5][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[3][1][0]} | {B[3][1][1]} | {B[3][1][2]} ‖‖ {B[4][1][0]} | {B[4][1][1]} | {B[4][1][2]} ‖‖ {B[5][1][0]} | {B[5][1][1]} | {B[5][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[3][2][0]} | {B[3][2][1]} | {B[3][2][2]} ‖‖ {B[4][2][0]} | {B[4][2][1]} | {B[4][2][2]} ‖‖ {B[5][2][0]} | {B[5][2][1]} | {B[5][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {B[6][0][0]} | {B[6][0][1]} | {B[6][0][2]} ‖‖ {B[7][0][0]} | {B[7][0][1]} | {B[7][0][2]} ‖‖ {B[8][0][0]} | {B[8][0][1]} | {B[8][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[6][1][0]} | {B[6][1][1]} | {B[6][1][2]} ‖‖ {B[7][1][0]} | {B[7][1][1]} | {B[7][1][2]} ‖‖ {B[8][1][0]} | {B[8][1][1]} | {B[8][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {B[6][2][0]} | {B[6][2][1]} | {B[6][2][2]} ‖‖ {B[7][2][0]} | {B[7][2][1]} | {B[7][2][2]} ‖‖ {B[8][2][0]} | {B[8][2][1]} | {B[8][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
  ‖===========‖===========‖===========‖
  ‖ Player: {player:s} ‖  Turn: {turn:<2d} ‖  Jing: {jing:s}  ‖
  ‖===========‖===========‖===========‖
  ‖ A | B | C ‖ {} | {} | {} ‖ 1 | 2 | 3 ‖
  ‖———|———|———‖———|———|———‖———|———|———‖
  ‖ D | E | F ‖ {} | {} | {} ‖ 4 | 5 | 6 ‖
  ‖———|———|———‖———|———|———‖———|———|———‖
  ‖ G | H | I ‖ {} | {} | {} ‖ 7 | 8 | 9 ‖
  ‖===========‖===========‖===========‖'''.format(
            seed   = self._GenerateSeed(),
            B = [[[self._Signs[self._Board[chr(i)]._subBoard[j][k]] for k in range(3)] for j in range(3)] for i in range(ord("A"), ord("J"))],
            # B = [[[self._Signs[self._Board[chr(i)]._finalBoard[j][k]] for k in range(3)] for j in range(3)] for i in range(ord("A"), ord("J"))], # use this to print the last status of the board, instead of all position captured
            player = self._Players[self._Player],
            turn   = self._Turn,
            jing   = self._Jing,
            *[self._Players[self._Board[chr(i)]._Owner] for i in range(ord("A"), ord("J"))],
        )
        print(output)
    # }}}1
# }}}1

default_config = {
    "signs": None,
    "first_player": None,
    "first_area": None,
}

Game = JiuJingQi(default_config)
Game._PrintBoard()
