from django import template

from sudokugame.models import Board
from sudokugame.sudoku_core import unflatten, generate, flatten, unflatten_split

register = template.Library()


@register.inclusion_tag('sudokugame/board.html')
def get_board(board=None, additional_cell_classes='', additional_board_classes=''):
    flattened = unflatten_split(board.grid, str, '0') if board else [['0' for i in range(9)] for i in range(9)]
    return {"grid": flattened,
            "cell_classes": additional_cell_classes,
            "board_classes": additional_board_classes}
