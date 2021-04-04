"""
This file provides multiple helper variables and methods for working with, generating, and solving Sudoku boards.
"""

import sys
from random import randrange
from sudoku import Sudoku

# Difficulty value represents the fraction of cells that are empty
difficulties = {
    'E': {'name': 'Easy', 'value': 1 - 37 / 81},
    'M': {'name': 'Medium', 'value': 1 - 27 / 81},
    'H': {'name': 'Hard', 'value': 1 - 17 / 81},
}


def generate(difficulty, seed=None):
    """
    Generate a sudoku board.
    :param difficulty: The key from the difficulties dictionary specifying the difficulty wanted.
    :param seed: The seed to use to generate the board, leave empty for random seed.
    """
    if seed is None:
      seed = randrange(sys.maxsize)
  
    difficulty_value = difficulties[difficulty]['value']
    return Sudoku(3, 3, seed=seed).difficulty(difficulty_value) 


def solve(board):
    """
    Solve a Sudoku board
    :param board: The sudoku board as a 2-dimensional array
    :return: The solution board as a 2-dimensional array
    """

    solution = Sudoku(3, 3, board=board).solve()
    return solution.board



def flatten(board):
    """
    Flatten a sudoku board. Converting the cell values into strings.
    The None variables are converted to "0".
    :param board: The sudoku board as a 2-dimensional array
    :return: The board passed in represented as a 1-dimensional array of strings, with "0" for emtpy cells.
    """

    return [str(cell) if cell is not None else '0' for row in board for cell in row]


def flatten_join(board):
    """
    Flatten the board, and then join the resulting array of strings together
    """

    return ''.join(flatten(board))


def unflatten(flattened_board, cast_fcn=int, zero_replace=None):
    """
    Inverse of the flatten() function.
    :param flattened_board: The sudoku board to unflatten as a 1-dimensional array of strings.
    :param cast_fcn: The type to cast the cells of the sudoku  board to
    :param zero_replace: What value to replace zero-values cells
    :return: The board passed represented as a 2-dimensional array
    """
    return [[cast_fcn(flattened_board[9 * i + j]) if flattened_board[9 * i + j] != '0' else zero_replace
             for j in range(9)] for i in range(9)]


def unflatten_split(board_str, cast_fcn=int, zero_replace=None):
    """
    Split the board string into an array of characters and then unflatten.
    Inverse of flatten_join()
    """
    return unflatten([c for c in board_str], cast_fcn, zero_replace)


def get_flattened_info(board):
    """
    Return the flattened board as well as the flattened solution of the given sudoku board
    :param board: The board to get the flattened info of.
    :return: A 2-tuple containing the flattened board and the flattened solution respecticely.
    """
    return flatten_join(board.board), flatten_join(board.solve().board)
