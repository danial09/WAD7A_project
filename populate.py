
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD7A_project.settings')

import django

django.setup()

from sudokugame.models import Board, Game
from sudokugame.sudoku_core import generate,flatten_join,solve
import datetime

def populate():

    # List of dictionaries containing data belonging to a model

    # Random username and scores
    users = [
        {'username': 'TestUsername1',
        'email' : 'testusername1@test.com',
        'score' : 900},
        {'username': 'TestUsername2',
        'email' : 'testusername2@test.com',
        'score' : 800},
        {'username': 'TestUsername3',
        'email' : 'testusername3@test.com',
        'score' : 500},
        {'username': 'TestUsername4',
        'email' : 'testusername4@test.com',
        'score' : 600},
        {'username': 'TestUsername5',
        'email' : 'testusername5@test.com',
        'score' : 100},
        {'username': 'TestUsername6',
        'email' : 'testusername7@test.com',
        'score' : 400},
        {'username': 'TestUsername8',
        'email' : 'testusername1@test.com',
        'score' : 700},
        {'username': 'TestUsername9',
        'email' : 'testusername9@test.com',
        'score' : 200},
        {'username': 'TestUsername10',
        'email' : 'testusername10@test.com',
        'score' : 1000},
    ]

    difficultiesC ='EMH'
    boards=[]

    for x in difficultiesC:
        board_base = generate(x,10)
        board = board_base.board
        solution = board_base.solve().board

        flattened_board = flatten_join(board)
        flattened_solution = flatten_join(solution)

        boardDict = {'grid': flattened_board,
                'solution': flattened_solution,
                'difficulty': x}
        boards.append(boardDict)

    date = datetime.date(2021,4,4)
    
    # add games
    for boardData in boards:
        b = addBoards(boardData['grid'], boardData['solution'], boardData['difficulty'])
        for userData in users:
            addGame(b, userData['username'],userData['score'],date)

    # print out the games we have added
    for b in Board.objects.all():
        for g in Game.objects.filter(id = b['id']):
            print(f'- {b}: {g}')     
    
    
# Function to add boards of different boards to the model
def addBoards(grid,solution,difficulty):
    b = Board.objects.get_or_create(grid = grid, solution = solution, difficulty = difficulty)
    b[0].save()
    return b

def addGame(b, username, score, date):
    g = Game.objects.get_or_create(board=b)
    g.user = username
    g.score = score
    g.date =date
    g.save()
    return g

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()