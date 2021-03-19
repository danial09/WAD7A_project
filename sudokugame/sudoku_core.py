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


def generate(difficulty):
    """
    Generate a sudoku board.
    :param difficulty: The key from the difficulties dictionary specifying the difficulty wanted.
    """

    difficulty_value = difficulties[difficulty]['value']
    return Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(difficulty_value)


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


def unflatten(flattened_board):
    """
    Inverse of the flatten() function.
    :param flattened_board: The sudoku board to unflatten as a 1-dimensional array of strings.
    :return: The board passed represented as a 2-dimensional array of ints, with None for empty cells
    """

    return [[int(flattened_board[9 * i + j]) if flattened_board[9 * i + j] != '0' else None
             for j in range(9)] for i in range(9)]
