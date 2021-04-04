from django import template

from sudokugame.models import Board
from sudokugame.sudoku_core import unflatten, generate, flatten, unflatten_split

register = template.Library()


@register.inclusion_tag('sudokugame/board.html')
def get_board(board=None, additional_cell_classes=''):
    if board is None:
        x = [['0' for i in range(9)] for i in range(9)]
        return {"grid": [['0' for i in range(9)] for i in range(9)], "cell_classes": additional_cell_classes}
    else:
        return {"grid": unflatten_split(board.grid, str, '0'), "cell_classes": additional_cell_classes}
