"""Noughts and Crosses assignment for CITS2401
   Modified by Naveed Akhtar
   28 Aug 2020
"""
from random import randint

# Define two constants, the values used to select a diagonal
TOP_LEFT_TO_BOTTOM_RIGHT = 0
TOP_RIGHT_TO_BOTTOM_LEFT = 1

# **********************************************************************
#
# Define all the functions that manipulate the board.
# Only these functions should 'know' the board representation.
# These functions don't "know" anything about noughts and crosses;
# only that it's played on a 3 x 3 board of 'O's and 'X's (and blanks).
#
# **********************************************************************
def create_board():
    """Create and return an empty board for Noughts and Crosses"""
    board = [ '', '', '', [ '', '', '']]
    pass


def display(board):
    """Display the given board"""
    separator = '+---+---+---+'
    print(separator)
    for row in board:
        print('|', end='')
        for col in row:
            print(' {} |'.format(col), end='')
        print('\n' + separator)
    print()


def cell(board, row, column):
    """Return the contents of the cell (row, column) of the board.
       The value is either 'O', 'X' or ' '
    """
    pass