#Othello

import collections

import math


NONE = 0
BLACK = 1
WHITE = 2
TIE = 3


class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass


class Board:
    def __init__(self, rows: int, columns: int, turn: str, top_left: str, winc: str):
        self._turn = turn
        self._winc = winc
        self._rows = rows
        self._columns = columns
        self._top_left = top_left
        self._board = self._new_game_board(turn)

        self.black_count = 0
        self.white_count = 0


    def put_disc(self, rows: int, columns: int) -> None:
        '''
        If there is a valid spot where disc(s) can be fliped, and
        the chosen spot is a valid spot to put the disc, it will
        put the disc and flip the disc at the same time. Then it will toss
        the turn to the other player. If not, it will let current player
        play again.
        '''
        
        self._require_valid_row_number(rows)
        self._require_valid_column_number(columns)
        self._require_game_not_over()
        
        if self.valid_flip() and self.is_valid_move(rows, columns):
            try:
                if self.flip_disc(rows, columns, make_a_flip = True):
                    print('VALID')
                    self._turn = self._opposite_turn(self._turn)

                else:
                    raise InvalidMoveError('INVALID')
                
            except InvalidMoveError:
                print('INVALID'),

        else:
            self._turn = self._opposite_turn(self._turn)



    def flip_disc(self, rows: int, columns: int, make_a_flip = True) -> None:
        '''
        Checks all 8 directions, and flips the disc.
        '''
        
        board = self._board
        direction = [[0, 1], [0, -1], [1, 0], [-1, 0],
                     [1, 1], [1, -1], [-1, 1], [-1, -1]]
        could_flip = False
        
        for row, col in direction:
            row_dir = rows
            col_dir = columns
            
            row_dir += row
            col_dir += col

            while self.onboard(row_dir, col_dir) and board[row_dir][col_dir] == self._opposite_turn(self._turn):
                row_dir += row
                col_dir += col

                if self.onboard(row_dir, col_dir) and board[row_dir][col_dir] == self._turn:
                    while True:
                        row_dir -= row
                        col_dir -= col

                        if row_dir == rows and col_dir == columns:
                            could_flip = True

                            if make_a_flip:
                                board[rows][columns] = self._turn
                            break
                        if make_a_flip:
                            board[row_dir][col_dir] = self._turn

        return could_flip

                        
    def valid_flip(self) -> bool:
        '''
        Returns True if there is a valid spot where disc(s) can be flipped.
        '''
        
        board = self._board

        for row in range(self._rows):
            for col in range(self._columns):
                if board[row][col] == NONE:
                    if self.flip_disc(row, col, make_a_flip = False):
                        return True
        return False
                                                 

    def onboard(self, rows: int, columns: int) -> bool:
        '''Return True if given row and column number is in the board.'''
        
        if rows < 0:
            return False
        elif rows >= self._rows:
            return False
        elif columns < 0:
            return False
        elif columns >= self._columns:
            return False
        else:
            return True

        
    def is_valid_move(self, rows: int, columns: int) -> bool:
        '''Returns True if the given row and column number is an empty spot.'''
        board = self._board
        if board[rows][columns] == NONE:
            return True
        else:
            return False

        
    def _new_game_board(self, top_left: str) -> [[int]]:
        '''Creates a new board according to given row and column numbers.'''

        board = []
        
        for row in range(self._rows):
            board.append([])
                
            for col in range(self._columns):
                board[-1].append(NONE)

        if top_left:
            board[math.floor(self._rows/2)][math.floor(self._columns/2)] = top_left
            board[math.floor(self._rows/2)-1][math.floor(self._columns/2)-1] = top_left
            board[math.floor(self._rows/2)][math.floor(self._columns/2)-1] = self._opposite_turn(top_left)
            board[math.floor(self._rows/2)-1][math.floor(self._columns/2)] = self._opposite_turn(top_left)
            

        self._board = board
        return board


    def print_board(self, rows: int, columns: int) -> None:
        board = self._board
        new_board = list(zip(*board))

        x = 1
        y = 1

        while x <= rows:
            print(end=' ')
            x += 1
        print()

        for i in new_board:
            unTupled = ' '.join(map(str, i))
            formattedLines = unTupled.replace('0', '.')
            print(formattedLines)



    def count_disc(self) -> None:
        '''Counts how many black and white discs are on the board, and
        returns the counts.'''
        
        board = self._board
        b_count = 0
        w_count = 0

        for row in range(self._rows):
            for col in range(self._columns):
                if board[row][col] == 'B':
                    b_count += 1
                elif board[row][col] == 'W':
                    w_count += 1
        self.black_count = b_count
        self.white_count = w_count
        
        return self.black_count, self.white_count
                    

    def _who_wins(self) -> None:
        '''Decides who wins according to user input: > or <.'''
        board = self._board

        if self.black_count > self.white_count:
            return BLACK
        elif self.white_count > self.black_count:
            return WHITE
        elif self.black_count == self.white_count:
            return TIE

    

    def winner(self) -> None:
        '''Determines the winner when the game is over.'''
        board = self._board
        winner = NONE

        if len(self.valid_spot()) == 0:
            if self._winc == '>':
                if self._who_wins() == BLACK:
                    winner = BLACK
                elif self._who_wins() == WHITE:
                    winner = WHITE
                elif self._who_wins() == TIE:
                    winner = TIE

            if self._winc == '<':
                if self._who_wins() == BLACK:
                    winner = WHITE
                elif self._who_wins() == WHITE:
                    winner = BLACK
                elif self._who_wins() == TIE:
                    winner = TIE
                    
        elif not self.valid_flip():
            self._turn = self._opposite_turn(self._turn)
            if not self.valid_flip():
                if self._winc == '>':
                    if self._who_wins() == BLACK:
                        winner = BLACK
                    elif self._who_wins() == WHITE:
                        winner = WHITE
                    elif self._who_wins() == TIE:
                        winner = TIE

                if self._winc == '<':
                    if self._who_wins() == BLACK:
                        winner = WHITE
                    elif self._who_wins() == WHITE:
                        winner = BLACK
                    elif self._who_wins() == TIE:
                        winner = TIE

        return winner


    def valid_spot(self) -> list:
        '''returns a list of empty spots.'''
        board = self._board
        valid_list = []

        for row in range(self._rows):
            for col in range(self._columns):
                if board[row][col] == NONE:
                    valid_list.append([row, col])

        return valid_list




    def change_player(self) -> None:
        '''changes the player.'''
        self._turn = self._opposite_turn(self._turn)

        
    def _opposite_turn(self, turn: str) -> str:
        '''Changes the turn to the other player.'''
        if turn == 'B':
            return 'W'
        else:
            return 'B'



    def whosTurn(self) -> str:
        '''displays whose turn it is.'''
        if self._turn.startswith('B'):
            return "Turn: B"

        if self._turn.startswith('W'):
            return "Turn: W"

        

    def checkWinner(self) -> bool:
        '''Checks the winner.'''
        if self.winner() == NONE:
            return False
        else:
            return True


    def printWinner(self):
        '''Prints the winner.'''
        gamewinner = self.winner()

        if gamewinner == BLACK:
            print('WINNER: BLACK')

        elif gamewinner == WHITE:
            print('WINNER: WHITE')

        elif gamewinner == TIE:
            print('WINNER: NONE')


    def _require_valid_row_number(self, rows: int) -> None:
        '''Raises a ValueError if its parameter is not a valid row number.'''
        if type(rows) != int or not self._is_valid_row_number(rows):
            raise ValueError('INVALID')


    def _require_valid_column_number(self, columns: int) -> None:
        '''Raises a ValueError if its paremeter is not a valid column number.'''
        if type(columns) != int or not self._is_valid_column_number(columns):
            raise ValueError('INVALID')


    def _require_game_not_over(self) -> None:
        '''Raises a GameOverError if the given game state represents a situation where
        the game is over.'''
        if self.winner() != NONE:
            raise GameOverError()


    def _is_valid_row_number(self, rows: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise.'''
        return 0 <= rows < self._rows


    def _is_valid_column_number(self, columns: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise.'''
        return 0 <= columns < self._columns


            
