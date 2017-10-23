import reversi_logic as reversi


def _user_action(board, rows: int, columns: int) -> None:
    '''
    takes the input from the user, then process proper action the user has input.
    Then prints the current counts of black and white, and prints the board.
    '''
    
    while True:
        try:
            action = board.put_disc(rows - 1, columns - 1)
            board.count_disc()
            print('B: {}  W: {}'.format(board.black_count, board.white_count))
            board.print_board(rows, columns)
            return action

        except InvalidMoveError:
            print('INVALID')



def _run_game(board) -> None:
    '''
    prompts the user to input where the user desires to put the disc, and plays the game
    until the winner is decided.
    '''
    
    while True:
        if not board.checkWinner():
            try:
                print('\n' + board.whosTurn())
                spot = input()
                game = _user_action(board, int(spot[-1]),
                                   int(spot[0]))

                if not board.valid_flip():
                    board.change_player()

            except ValueError:
                print('INVALID')

            except reversi.InvalidMoveError:
                return

            if len(board.valid_spot()) == 0:
                board.printWinner()
                return
                
        else:
            board.printWinner()
            return

        
def _play_reversi(rows: int, columns: int, turn: str, top_left: str, winc: str) -> None:
    '''
    Takes input from the user and sets up the game according to
    user input. Then runs the game.
    '''

    board = reversi.Board(rows, columns, turn, top_left, winc)

    valid_numbers = [2, 4, 6, 8, 10, 12, 14, 16]


    if int(rows) in valid_numbers and int(columns) in valid_numbers:
        board.count_disc()
        print('B: {}  W: {}'.format(board.black_count, board.white_count))
        board.print_board(rows, columns)
        _run_game(board)
        
    else:
        return


    
        
        
if __name__ == '__main__':
    print('FULL')

    valid_numbers = [2, 4, 6, 8, 10, 12, 14, 16]
    
    try:
        BOARD_ROWS = int(input())
        BOARD_COLUMNS = int(input())
        BOARD_TURN = input()
        BOARD_TOP_LEFT = input()
        BOARD_WINC = input()
        
        if int(BOARD_ROWS) in valid_numbers and int(BOARD_COLUMNS) in valid_numbers:
            _play_reversi(BOARD_ROWS, BOARD_COLUMNS, BOARD_TURN, BOARD_TOP_LEFT, BOARD_WINC)
            
        else:
            raise ValueError('Invalid row number. Please enter even integer between 2 and 16.')

    except ValueError:
        print('Invalid row number. Please enter even integer between 2 and 16.')




