# Author: Alexandre Steinhauslin
# Description: An Othello boardgame

"""CONSTANTS"""
BLACK_PIECE = 'X'
WHITE_PIECE = 'O'
EDGE = '*'
EMPTY_SPACE = '.'

# Hor = Horizontal, Ver = Vertical, Diag = Diagonal, Do = down, Ri = Right, Le = Left
#                   Hor Left,Hor Right, Ver Up  , Ver Down, Diag Do Le, Diag Up Ri, Diag Do Ri, Diag Up Le
BOARD_DIRECTIONS = [[0, '-'], [0, '+'], ['-', 0], ['+', 0], ['+', '-'], ['-', '+'], ['-', '-'], ['+', '+']]


class InvalidColor(Exception):
    """Raises an exception if an invalid color is passed"""
    pass


def sort_list_of_tuples(the_list):
    """sorts the_list of tuples in ascending order based on the x value then the y"""
    sorted(the_list)


class Player:
    """The player class. Two players play a game. Each player has a name and a color"""
    _name = None
    _color = None

    def __init__(self, name, color):
        """Constructor for the player"""
        self._name = name
        self._color = color.upper()

    def get_name(self):
        """returns player's name"""
        return self._name

    def get_color(self):
        """returns player's color"""
        return self._color


class Othello:
    _player_no_moves = []  # a list of all the players that can't make a move
    _player_list = []  # list of players, max of 2
    _winner = ""

    def __init__(self):
        """Othello constructor"""
        self._board = [
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
            ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ]

    def print_board(self):
        """Prints out the board as it currently is"""
        num_row = len(self._board)
        num_col = len(self._board[0])
        print('\n')
        print('  ', end='')
        for number in range(num_col):  # print column numbers
            print(str(number) + '    ', end='')
        print()
        for row in range(num_row):
            print(str(row) + ' ', end='')
            for col in range(num_col):
                print(self._board[row][col] + '    ', end='')
            if row != (num_row - 1):
                print()
            print()

    def create_player(self, player_name, color):
        """Creates a player to play the game"""
        if len(self._player_list) == 2:
            print("Sorry, Maximum 2 players per game")
        else:
            self._player_list.append(Player(player_name, color))

    def print_players(self):
        print("The", self._player_list[0].get_color(), "player is", self._player_list[0].get_name())
        print("The", self._player_list[1].get_color(), "player is", self._player_list[1].get_name())

    def piece_counter(self, piece):
        """counts the number of instances on a board of a given piece"""
        counter = 0
        side = len(self._board[0])
        for y in range(side):
            for x in range(side):
                if self._board[y][x] == piece:
                    counter += 1
        return counter

    def piece_positions(self, color):
        """return_available_positions helper function
        finds all the positions of the given color and returns them as a coordinate value list"""
        positions = []
        piece = WHITE_PIECE if color.upper() == 'WHITE' else BLACK_PIECE
        side = len(self._board[0])
        for x in range(side):
            for y in range(side):
                if self._board[x][y] == piece:
                    positions.append([x, y])
        return positions

    def return_winner(self):
        """prints out who is the winner or if there is a tie"""
        if self._player_list[0].get_color() == 'WHITE':
            white_player_name = self._player_list[0].get_name()
            black_player_name = self._player_list[1].get_name()
        else:
            white_player_name = self._player_list[1].get_name()
            black_player_name = self._player_list[0].get_name()

        if self._winner == 'TIE':
            return "It's a tie"
        elif self._winner == 'WHITE':
            return "Winner is white player: " + white_player_name
        else:
            return "Winner is black player: " + black_player_name

    def return_available_positions(self, color):
        """takes in a color and returns possible moves for that player
        this function calls the piece_positions and then the scan_for_moves method,
        will also check to make sure there are no duplicate coordinates"""
        if color.upper() != "WHITE" and color.upper() != "BLACK":
            raise InvalidColor("must choose a valid color")
        color_positions = self.piece_positions(color)  # get all positions of single color pieces
        result = []

        for single_position in color_positions:
            answer = self.scan_for_moves(single_position)  # scan for moves deriving from a single piece
            result.extend(answer)

        no_duplicates = []
        for item in result:
            if item not in no_duplicates:  # check if we already saved those coordinates, we don't want doubles
                no_duplicates.append(item)

        return sorted(no_duplicates)

    def scan_for_moves(self, coordinates):
        """this is a helper function for the return_available_positions
        coordinates will be a single piece coordinates in this format [x, y]
        it returns al possible moves that stem from that specific tile
        it won't return anything if none are available"""
        row = coordinates[0]
        column = coordinates[1]

        coordinates_piece_color = WHITE_PIECE if self._board[row][column] == WHITE_PIECE else BLACK_PIECE
        opponent_color = WHITE_PIECE if coordinates_piece_color == BLACK_PIECE else BLACK_PIECE
        possible_moves = []

        def unidirectional_scanner(row_change, column_change):
            """takes in a +, -, or 0
            scans all possible moves in a specific direction, if there are any they will be appended to possible_moves
            and returned all together"""
            passed_an_opponents_tile = False

            def single_step(change):
                if change == 0:
                    return 0
                elif change == '-':
                    return -1
                elif change == '+':
                    return 1

            row_single_step = single_step(row_change)
            column_single_step = single_step(column_change)

            for index in range(1, len(self._board[0])):
                if (self._board[row + row_single_step][column + column_single_step] == EDGE) or (
                        self._board[row + row_single_step][column + column_single_step] == EMPTY_SPACE):
                    # there are no moves in this direction
                    break
                # START TRANSVERSING
                # if find a piece of same color or an edge you are done
                if (self._board[row + (index * row_single_step)][column + (
                        index * column_single_step)] == coordinates_piece_color) or (
                        self._board[row + (index * row_single_step)][column + (index * column_single_step)] == EDGE):
                    break
                # if find opposite color keep going
                elif self._board[row + (index * row_single_step)][column + (
                        index * column_single_step)] == opponent_color:
                    passed_an_opponents_tile = True
                    continue
                # if after you found at least one opposite color you find an empty slot then that is a move
                elif (self._board[row + (index * row_single_step)][column + (
                        index * column_single_step)] == EMPTY_SPACE) and passed_an_opponents_tile:
                    return row + (index * row_single_step), column + (index * column_single_step)

        for directions in BOARD_DIRECTIONS:
            result = unidirectional_scanner(directions[0], directions[1])
            if result:
                possible_moves.append(result)

        return possible_moves

    def flip_pieces(self, player_piece, coordinates, opponent_piece):
        """gets called by the make_move method to flip the pieces of the board
        coordinates come in 2d form already
        scans in which directions the opponent is and flips all the pieces until it find its same color"""
        row = coordinates[0]
        column = coordinates[1]

        def unidirectional_flipper(row_change, column_change):
            """takes in a +, -, or 0
            scans all flippable pieces in a specific direction, if there are any they will be flipped"""
            potential_flips = []  # as we travers the direction we take into account the pieces to potentially flip

            def single_step(change):
                if change == 0:
                    return 0
                elif change == '-':
                    return -1
                elif change == '+':
                    return 1

            row_single_step = single_step(row_change)
            column_single_step = single_step(column_change)

            for index in range(1, len(self._board[0])):
                # if the first tile is empty or edge we are done
                if (self._board[row + row_single_step][column + column_single_step] == EDGE) or (
                        self._board[row + row_single_step][column + column_single_step] == EMPTY_SPACE):
                    # there are no flips in this direction
                    break
                # START TRAVERSING
                # if find an empty space or an edge you are done
                if (self._board[row + (index * row_single_step)][column + (index * column_single_step)] == EDGE) or (
                        self._board[row + (index * row_single_step)][column + (
                                index * column_single_step)] == EMPTY_SPACE):
                    break
                # if find opposite color keep going and add it to potential_flips
                elif self._board[row + (index * row_single_step)][column + (
                        index * column_single_step)] == opponent_piece:
                    # passed_an_opponents_tile = True
                    potential_flips.append([row + (index * row_single_step), column + (index * column_single_step)])
                    continue
                # if after you found at least one opposite color you find a player_piece then potential_flips are flips!
                elif self._board[row + (index * row_single_step)][column + (
                        index * column_single_step)] == player_piece:
                    # flip
                    for flip in potential_flips:
                        # self._board[flip[0]][flip[1]] = player_piece
                        self._board[flip[0]][flip[1]] = player_piece
                    return "Pieces Flipped"

        for directions in BOARD_DIRECTIONS:
            unidirectional_flipper(directions[0], directions[1])

    def make_move(self, color, piece_position):
        """makes a move for the player to the given position, only valid positions will be passed"""
        """since it's a piece position given by the player I will assume that it is in x,y format"""
        row = piece_position[0]
        column = piece_position[1]
        player_piece = WHITE_PIECE if color.upper() == 'WHITE' else BLACK_PIECE
        opponent_piece = WHITE_PIECE if player_piece == BLACK_PIECE else BLACK_PIECE

        self._board[row][column] = player_piece
        self.flip_pieces(player_piece, (row, column), opponent_piece)

        return self._board

    def play_game(self, player_color, piece_position):
        """attempts to make the player_color player make a move at piece_position
        it will either return invalid move, print a message, and return valid moves
        OR make the move by calling make_move
        when all the tiles on the board are taken, his is when the return_winner method will be called"""
        possible_moves = self.return_available_positions(player_color)

        if piece_position in possible_moves:  # it's a valid move, let's make it happen!
            self.make_move(player_color, piece_position)
            white_count, black_count = self.piece_counter(WHITE_PIECE), self.piece_counter(BLACK_PIECE)
            # NEXT PLAYER'S TURN

            if white_count + black_count == 64:  # then the board is full and the game is over
                print("Game is ended with white piece:", white_count, "black piece:", black_count)
                if white_count > black_count:
                    self._winner = "WHITE"
                elif black_count > white_count:
                    self._winner = "BLACK"
                else:
                    self._winner = "TIE"

                print(self.return_winner())

        else:  # piece_position not in possible_moves:
            print("Here are the valid moves:", possible_moves)
            return "Invalid move"
            # THIS PLAYER SHOULD TRY AGAIN

    def random_game(self):
        """random game generator for testing"""

        def white_turn():
            possible_moves = self.return_available_positions('white')
            self.play_game('white', possible_moves[(len(possible_moves) // 2)])

        def black_turn():
            possible_moves = self.return_available_positions('black')
            self.play_game('black', possible_moves[(len(possible_moves) // 2)])

        for x in range(29):
            white_turn()
            black_turn()

game_1 = Othello()
game_1.create_player("Wilson", "white")
game_1.create_player("Barry", "bLaCk")
game_1.print_players()
game_1.print_board()
#
# game_1.random_game()
#
game_1.play_game('black', (3, 4))
game_1.print_board()

game_1.play_game('white', (3, 3))
game_1.play_game('black', (4, 3))
game_1.play_game('white', (5, 3))
game_1.print_board()

# print(game_1.return_available_positions('whIte'))

# -----
# game_1.play_game('black', (1, 2))
# print(game_1.play_game('white', (8, 8)))
# print(game_1.play_game('black', (8, 8)))
# # -----

# game = Othello()
# game.print_board()
# game.create_player("Helen", "white")
# game.create_player("Leo", "black")
# game.play_game("black", (6,5))
# game.print_board()
# game.play_game("white", (6,6))
# game.print_board()