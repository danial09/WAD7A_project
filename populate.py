
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
    eboard = generate('E',10)
    mboard = generate('M',10)
    hboard =generate('H',10)

    boards = [{'grid': flatten_join(eboard),
                'solution': flatten_join(solve(eboard)),
                'diffiulty': 'E'},
                {'grid': flatten_join(hboard),
                'solution': flatten_join(solve(hboard)),
                'difficulty': 'H'},
                {'grid': flatten_join(mboard),
                'solution': flatten_join(solve(mboard)),
                'difficulty': 'M'}
                ]

    date = datetime.date(2021,4,4)
    
    # add games
    for boardData in boards.itens():
        b = addBoards(boardData.get('grid'), boardData.get('solution'), boardData.get('difficulty'))
        for userData in user.items():
            g = addGame(userData.get('username'), b['id'],b['difficulty'],userData.get('score'),date)

    # print out the games we have added
    for b in Board.objects.all():
        for g in Game.objects.filter(id = b['id']):
            print(f'- {b}: {g}')     
    
    
# Function to add boards of different boards to the model
def addBoards(grid,solution,difficulty):
    b = Board.objects.get_or_create(grid = grid, solution = solution, difficulty = difficulty)
    b.save()
    return b

def addGame(username, id, difficulty, score, date):
    g = Game.objects.get_or_create(username, id, difficulty, score, date)
    g.save()
    return g

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()