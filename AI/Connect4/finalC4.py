import math
import random
import copy

# Global constants
ROWS = 6
COLUMNS = 7
WINDOW_LENGTH = 4

# Create board for the Game
def create_board():
    board = [[""] * ROWS for i in range(COLUMNS)]
    return board
    

class C4Agent:
    """"
    Connect4 Agent for CITS3001 Lab 6

    This method is given:
        a symbol ('X' or 'O' indicating which discs are the players), 
        a board (a list of 7 strings, each string representing a column of the game with the first character being the bottom row, 
            made up of the characters 'X' and 'O'. 
            Note that  the strings are initially empty and grow throughout the game to a maximum length of 6.
        your opponents last move (the index of a column they dropped the disc into, or -1 if it is the first move).
    The method returns the index of the column your strategy chooses to put the disc into. Note if your method returns a column outside the range [0-6] 
    or tries to put a disc into a full column, it automatically loses.

    The first test method will pitch your agent against a random opponent four times, 
    and your agent needs to win all games to pass. At the end of the game you are given a string representation of the board. 
    Your discs are labelled 'A', 'B', 'C',... and the opponents are 'a','b','c',... 
    so you can infer the order they were played. 

    The second test requires your agent to beat a simple 2 ply minimax agent.
    
    """

    def __init__(self) -> None:
        global player_AI
        global player_Opponent_AI
        global current_board

        current_board = create_board()

        # Current symbol is undefined in the beginning
        player_AI = ""
        player_Opponent_AI = ""


    def dropSymbol(board, column, row, symbol):
        # Drop a piece at the given position of the board
        board[column][row] = symbol
    
    def is_valid(self, board, col):
        # Check if the current pos is valid
        return board[col][-1] == ""

    def availableRows(self, board, col):
        # Get next available row
        for row in range(ROWS):
            if board[col][row] == '':
                return row

    def availableColumns(self, board):
        # Get next available column
        result = [] 
        for column in range(COLUMNS):
            if self.is_valid(board, column):
                result.append(column)
        return result

                
    def checkWin(self, board, symbol):
        # Checks if the game has ended and who has won
        # Or if there are no possible moves left

        # Check for 4 straight horizontally
        for row in range(ROWS):
            for column in range(COLUMNS - 3):
                if board[column][row] == symbol and board[column + 1][row] == symbol and board[column + 2][row] == symbol and board[column + 3][row] == symbol:
                    return True

        # Check for 4 straight vertically
        for row in range(ROWS - 3):
            for column in range(COLUMNS):
                if board[column][row] == symbol and board[column][row + 1] == symbol and board[column][row + 2] == symbol and board[column][row + 3] == symbol:
                    return True

        # Check for 4 straight diagonally (+)(/)
        for row in range(ROWS - 3):
            for column in range(COLUMNS - 3):
                if board[column][row] == symbol and board[column + 1][row + 1] == symbol and board[column + 2][row + 2] == symbol and board[column + 3][row + 3] == symbol:
                    return True

        # Check for 4 straight horizontally (-)(\)
        for row in range(3, ROWS):
            for column in range(COLUMNS - 3):
                if board[column][row] == symbol and board[column + 1][row - 1] == symbol and board[column + 2][row - 2] == symbol and board[column + 3][row - 3] == symbol:
                    return True

    def check_window(self, window, symbol):
        score = 0

        if window.count(symbol) == 4:
            score += 100
        elif window.count(symbol) == 3 and window.count("") == 1:
            score += 5
        elif window.count(symbol) == 2 and window.count("") == 2:
            score += 2
        
        if window.count(player_Opponent_AI) == 3 and window.count("") == 1:
            score -= 4
        return score

    def scores(self, board, symbol):
        # For score positions

        # scores
        result = 0

        center_arr = board[COLUMNS // 2]
        count_center = center_arr.count(symbol)
        result += count_center * 3

        # Horizontal
        for row in range(ROWS) :
            #row_array = [int(i) for i in list(board[row,:])]
            row_array = [col[row] for col in board]

            window = row_array[:WINDOW_LENGTH]

            right = 3

            result += self.check_window(window, symbol)

            while right < COLUMNS - 1:
                right += 1
                window.append(row_array[right])
                window.pop(0)
                result += self.check_window(window, symbol)
        

        # Vertical
        for columns in board:
            window = columns[:WINDOW_LENGTH]
            up = 3
            result += self.check_window(window, symbol)
            while up < ROWS - 1:
                up += 1
                window.append(columns[up])
                window.pop(0)
                result += self.check_window(window, symbol)

        # Positive diagonal
        for row in range(ROWS - 3):
            for column in range(COLUMNS - 3):
                window = [board[column + i][row + i] for i in range(WINDOW_LENGTH)]
                result += self.check_window(window, symbol)

        # Negative diagonal
        for column in range(3, COLUMNS):
            for row in range(ROWS - 3):
                window = [board[column - 3 + i][row + i] for i in range(WINDOW_LENGTH)]
                result += self.check_window(window, symbol)

        return result
    
    def gameFin(self, board):
        return self.checkWin(board, player_AI) or self.checkWin(board, player_Opponent_AI) or len(self.availableColumns(board)) == 0 

    def minimaxAlgo(self, board, depth, alpha, beta, maxPlayer):
        '''
        MaximisingPlayer will try to maximize the value
        Min will choose whatever value is the minimum. 
        The algorithm performs a depth-first search (DFS) 
        '''

        # Array which includes possible columns to place piece
        possible_locations = self.availableColumns(board)
        
        # Check whether the node is a terminal node 
        is_terminal = self.gameFin(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.checkWin(board, player_Opponent_AI):
                    return (None, 1000000000)
                elif self.checkWin(board, player_AI):
                    return (None, 1000000000)
                else:
                    return (None, 0)
            else:
                return(None, self.scores(board, player_AI))

        if maxPlayer:
            val = -math.inf
            column = random.choice(possible_locations)
            for col in possible_locations:
                row = self.availableRows(board, col)
                board_copy = copy.deepcopy(board)
                board_copy[col][row] = player_AI
                #C4Agent.dropSymbol(board_copy, col, row, player_AI)
                new_score = self.minimaxAlgo(board_copy, depth-1, alpha, beta, False)[1]
                if new_score > val:
                    val = new_score
                    column = col
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return column, val

        else:
            # Minimising player
            val = math.inf
            column = random.choice(possible_locations)
            for col in possible_locations:
                row = self.availableRows(board, col)
                board_copy = copy.deepcopy(board)
                board_copy[col][row] = player_Opponent_AI
                #C4Agent.dropSymbol(board_copy, col, row, player_AI)

                new_score = self.minimaxAlgo(board_copy, depth-1, alpha, beta, True)[1]
                if new_score < val:
                    val = new_score
                    column = col
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return column, val
    
            

    def move(self, symbol, board, last_move):
        '''
        symbol is the character that represents the agents moves in the board.
        symbol will be consistent throughout the game
        board is an array of 7 strings each describing a column of the board
        last_move is the column that the opponent last droped a piece into (or -1 if it is the firts move of the game).
        This method should return the column the agent would like to drop their token into.
        '''
        global player_Opponent_AI
        global player_AI


        if symbol == "O":
            player_Opponent_AI = "X"
            player_AI = "O"
        else:
            player_Opponent_AI = "O"
            player_AI = "X"

        if last_move != -1:
            row = self.availableRows(current_board, last_move)
            current_board[last_move][row] = player_Opponent_AI
            #C4Agent.dropSymbol(current_board, last_move, row, player_Opponent_AI)


        col, score = self.minimaxAlgo(current_board, 3, -math.inf, math.inf, True)
        row = self.availableRows(current_board, col)
        current_board[col][row] = symbol
        #C4Agent.dropSymbol(current_board, col, row, symbol)
        return col