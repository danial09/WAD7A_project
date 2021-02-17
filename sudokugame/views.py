import sys
from random import randrange

from django.shortcuts import render

from sudoku import Sudoku


# Create your views here.

def test(request):
    puzzle = Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(0.7)
    flattened = [str(cell) if cell is not None else '0' for row in puzzle.board for cell in row]

    return render(request, 'sudokugame/test.html', context={'board': flattened})
