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
        config (dict, optional): Configures for the Jing. Defaults to {"owner": None, "board": None}.

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
    def __init__(self, config: dict = {"owner": None, "board": None}):
        """Initializes the Jing.
        
        Arguments:
            config (dict, optional): Configures for the Jing. Defaults to {"owner": None, "board": None}.
        """
        self._Owner = 0 if config["owner"] is None else config["owner"]
        self._subBoard = [[0 for i in range(3)] for j in range(3)] if config["board"] is None else config["board"]
        self._finalBoard = self._subBoard
        self._Captured = self._HaveCaptured()
        self._CheckOwner()

    def _HaveCaptured(self) -> list[int]:
        """Returns the number of captured positions in the Jing.

        Returns:
            [empty, first_player, second_player] (list): The number of captured positions in the Jing for each player.
        """
        captured = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                captured[self._subBoard[i][j]] += 1
        return captured

    def _Capture(self, player: int, position: tuple[int, int]):
        """Captures a position in the Jing.
        
        Arguments:
            player   (int):   The player who captures the position.
            position (tuple): The position to be captured.

        Returns:
            1: The position is captured successfully.
            0: The position is not captured successfully.
        """
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

    def _CheckValid(self, position: tuple[int, int]):
        """Checks if the position to be captured is valid.

        Arguments:
            position (tuple): The position to be captured.

        Returns:
            1: The position is valid.
            0: The position is invalid.
        """
        return self._Owner == 0 and self._subBoard[position[0]][position[1]] == 0

    def _CheckOwner(self):
        """Checks if the Jing has an owner. If so, occupy the Jing.

        Returns:
            1: The Jing is occupied.
            0: The Jing is not occupied.
        """
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
        """Occupies the Jing.

        Arguments:
            player (int): The player who occupies the Jing.

        Returns:
            1: The Jing is occupied.
            0: The Jing is not occupied.
        """
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
        _History (dict):  The history of the game.
        _Move    (dict):  The history of moves of players.
        _Player  (int):   The current player.
        _Turn    (int):   The current turn.
        _Jing    (str):   The current jing.

    Methods:
        _GenerateSeed: Generates a seed of the current board.
        _UnpackSeed:   Unpacks a seed to the current board.
        _Ord2Jing:     Converts an order to a Jing.
        _CheckWinner:  Checks if there's a winner.
        _PrintBoard:   Prints the board.
    """
    def __init__(self, config: dict = {}): # {{{1 JiuJingQi Init
        """Initializes the game.

        Arguments:
            config (dict, optional): Configures for the game. Defaults to {}.
        """
        self._CONST()

        self._Config = config
        self._Signs = self._Config["signs"] or self.DEFAULT_SIGNS
        self._Players = [sign for sign in self._Signs]
        self._Board = {chr(i): Jing({
            "owner": None,
            "board": None,
            # "board": [[random.randint(0, 2) for i in range(3)] for j in range(3)],  # Random board to test
            }) for i in range(ord("A"), ord("J"))}
        self._History = {1: [], 2: []}
        self._Move = {1: [], 2: []}
        self._Player = 1 if self._Config["first_player" ]is None else self._Config["first_player"]
        self._Turn = 1
        self._Jing = "?" if self._Config["first_area"] is None else self._Config["first_area"]
    # }}}1

    def _GenerateSeed(self): # {{{1 GenerateSeed
        """Generates a seed of the current board.

        Returns:
            seed (str): The seed of the current board.
        """
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
        """Unpacks a seed to the current board.

        Arguments:
            seed (str): The seed to be unpacked.

        Returns:
            status (bool): Whether the seed is valid.
            code   (int):  The error code. 0 for no error.
            player (int):  The player of the game.
            jing   (str):  The current Jing of the game.
            board  (dict): The board of the game.
        """
        try:
            if len(seed) != 29:
                raise Exception("Invalid seed length.")
            player = int(seed[0])
            jing = seed[1]
            board = {chr(i): Jing() for i in range(ord("A"), ord("J"))}
            seed_map = {"0": "000", "A": "001", "B": "002", "C": "010", "D": "011", "E": "012", "F": "020", "G": "021", "H": "022", "I": "100", "J": "101", "K": "102", "L": "110", "M": "111", "N": "112", "O": "120", "P": "121", "Q": "122", "R": "200", "S": "201", "T": "202", "U": "210", "V": "211", "W": "212", "X": "220", "Y": "221", "Z": "222"}
            for i in range(2, 29):
                row_map = seed_map[seed[i]]
                for j in range(3):
                    board[self._Ord2Jing(i // 3)]._subBoard[(i - 2) % 3][j] = int(row_map[j])
            return {
                "status": True,
                "code":   0,
                "player": player,
                "jing":   jing,
                "board":  board,
            }
        except:
            # TODO: Raise an error
            return {
                "status": False,
                "code":   1,
                "player": None,
                "jing":   None,
                "board":  None,
            }
    # }}}1

    def _Ord2Jing(self, order: int): # {{{1 Order2Jing
        """Converts an order to a Jing.

        Arguments:
            order (int): The order to be converted.

        Returns:
            jing (str): The Jing of the order.
        """
        return chr(ord("A") + order)
    # }}}1

    def _Ord2Position(self, order: int): # {{{1 Order2Position
        """Converts an order to a position.

        Arguments:
            order (int): The order to be converted.

        Returns:
            position (tuple): The position of the order.
        """
        return (order // 3, order % 3)
    # }}}1

    def _CheckWinner(self, board): # {{{1 CheckWinner
        """Checks if there's a winner.

        Arguments:
            board (dict): The board to be checked.

        Returns:
            1: Player 1 wins.
            2: Player 2 wins.
            0: No one wins.
        """
        for i in range(3):
            row_result = board[self._Ord2Jing(i * 3)]._Owner & board[self._Ord2Jing(i * 3 + 1)]._Owner & board[self._Ord2Jing(i * 3 + 2)]._Owner
            col_result = board[self._Ord2Jing(i)]._Owner & board[self._Ord2Jing(i + 3)]._Owner & board[self._Ord2Jing(i + 6)]._Owner
            if row_result == 1 or col_result == 1:
                return 1
            elif row_result == 2 or col_result == 2:
                return 2
        diag_result_1 = board["A"]._Owner & board["E"]._Owner & board["I"]._Owner
        diag_result_2 = board["C"]._Owner & board["E"]._Owner & board["G"]._Owner
        if diag_result_1 == 1 or diag_result_2 == 1:
            return 1
        elif diag_result_1 == 2 or diag_result_2 == 2:
            return 2
        return 0
    # }}}1

    def _PrintBoard(self): # {{{1 PrintBoard
        """Prints the board.
        """
        print('''seed={seed:s}
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {Board[0][0][0]} | {Board[0][0][1]} | {Board[0][0][2]} ‖‖ {Board[1][0][0]} | {Board[1][0][1]} | {Board[1][0][2]} ‖‖ {Board[2][0][0]} | {Board[2][0][1]} | {Board[2][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[0][1][0]} | {Board[0][1][1]} | {Board[0][1][2]} ‖‖ {Board[1][1][0]} | {Board[1][1][1]} | {Board[1][1][2]} ‖‖ {Board[2][1][0]} | {Board[2][1][1]} | {Board[2][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[0][2][0]} | {Board[0][2][1]} | {Board[0][2][2]} ‖‖ {Board[1][2][0]} | {Board[1][2][1]} | {Board[1][2][2]} ‖‖ {Board[2][2][0]} | {Board[2][2][1]} | {Board[2][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {Board[3][0][0]} | {Board[3][0][1]} | {Board[3][0][2]} ‖‖ {Board[4][0][0]} | {Board[4][0][1]} | {Board[4][0][2]} ‖‖ {Board[5][0][0]} | {Board[5][0][1]} | {Board[5][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[3][1][0]} | {Board[3][1][1]} | {Board[3][1][2]} ‖‖ {Board[4][1][0]} | {Board[4][1][1]} | {Board[4][1][2]} ‖‖ {Board[5][1][0]} | {Board[5][1][1]} | {Board[5][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[3][2][0]} | {Board[3][2][1]} | {Board[3][2][2]} ‖‖ {Board[4][2][0]} | {Board[4][2][1]} | {Board[4][2][2]} ‖‖ {Board[5][2][0]} | {Board[5][2][1]} | {Board[5][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖===========‖‖===========‖‖===========‖‖
‖‖ {Board[6][0][0]} | {Board[6][0][1]} | {Board[6][0][2]} ‖‖ {Board[7][0][0]} | {Board[7][0][1]} | {Board[7][0][2]} ‖‖ {Board[8][0][0]} | {Board[8][0][1]} | {Board[8][0][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[6][1][0]} | {Board[6][1][1]} | {Board[6][1][2]} ‖‖ {Board[7][1][0]} | {Board[7][1][1]} | {Board[7][1][2]} ‖‖ {Board[8][1][0]} | {Board[8][1][1]} | {Board[8][1][2]} ‖‖
‖‖———|———|———‖‖———|———|———‖‖———|———|———‖‖
‖‖ {Board[6][2][0]} | {Board[6][2][1]} | {Board[6][2][2]} ‖‖ {Board[7][2][0]} | {Board[7][2][1]} | {Board[7][2][2]} ‖‖ {Board[8][2][0]} | {Board[8][2][1]} | {Board[8][2][2]} ‖‖
‖‖===========‖‖===========‖‖===========‖‖
  ‖===========‖===========‖===========‖
  ‖ Player: {player:s} ‖  Turn: {turn:<2d} ‖  Jing: {jing:s}  ‖
  ‖===========‖===========‖===========‖
  ‖ A | B | C ‖ {Jing[0]} | {Jing[1]} | {Jing[2]} ‖ 1 | 2 | 3 ‖
  ‖———|———|———‖———|———|———‖———|———|———‖
  ‖ D | E | F ‖ {Jing[3]} | {Jing[4]} | {Jing[5]} ‖ 4 | 5 | 6 ‖
  ‖———|———|———‖———|———|———‖———|———|———‖
  ‖ G | H | I ‖ {Jing[6]} | {Jing[7]} | {Jing[8]} ‖ 7 | 8 | 9 ‖
  ‖===========‖===========‖===========‖'''.format(
            # Board = [[[self._Signs[self._Board[chr(i)]._finalBoard[j][k]] for k in range(3)] for j in range(3)] for i in range(ord("A"), ord("J"))], # use this to print the last status of the board, instead of all position captured
            Board = [[[self._Signs[self._Board[chr(i)]._subBoard[j][k]] for k in range(3)] for j in range(3)] for i in range(ord("A"), ord("J"))],
            Jing   = [self._Players[self._Board[chr(i)]._Owner] for i in range(ord("A"), ord("J"))],
            seed   = self._GenerateSeed(),
            player = self._Players[self._Player],
            turn   = self._Turn,
            jing   = self._Jing,
        ))
    # }}}1

    def _CONST(self): # {{{1 CONST
        """Defines the constants.
        """
        self.DEFAULT_SIGNS = (" ", "X", "O")
    # }}}1
# }}}1

default_config = {
    "signs": None,
    "first_player": None,
    "first_area": None,
}

Game = JiuJingQi(default_config)
Game._PrintBoard()
