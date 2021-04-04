import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD7A_project.settings')

import django

django.setup()

from sudokugame.models import Board, Game
from sudokugame.sudoku_core import generate, flatten_join, solve
from django.utils import timezone
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta


def populate():
    # List of dictionaries containing data belonging to a model

    # Random username and scores
    users = [
        {'username': 'TestUsername1',
         'email': 'testusername1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername2',
         'email': 'testusername2@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername3',
         'email': 'testusername3@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername4',
         'email': 'testusername4@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername5',
         'email': 'testusername5@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername6',
         'email': 'testusername7@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername8',
         'email': 'testusername1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
         {'username': 'TestUsername9',
         'email': 'testusername9@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername10',
         'email': 'testusername10@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername11',
         'email': 'testusername11@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername12',
         'email': 'testusername12@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername13',
         'email': 'testusername13@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername14',
         'email': 'testusername14@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'TestUsername15',
         'email': 'testusername15@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
    ]
    scoreEasy = [1223, 1244, 4144, 5551, 1233, 54234, 554234, 12313, 41241, 2342, 1231, 4124, 74655, 100]
    scoreMedium =[1223, 4124, 74655, 100, 41241, 554234, 1244,  2342, 1231, 1233, 54234, 4144, 5551, 12313,]
    scoreHard = [4124, 74655, 100, 1223,  4144, 5551, 12313, 41241, 554234, 1244,  2342, 1231, 1233, 54234]
    scoreDC = [1223,  554234, 4124,4144, 5551, 74655, 41241, 2342, 1231, 1233, 100,1244,  12313, 54234]

    # different dates to test teh daily, weekly and monthly leaderboard
    date = timezone.now()
    dates = [date, date - relativedelta(days=1), date - relativedelta(weeks=1), date - relativedelta(months=1)]
    difficultiesC = 'EMH'
    boards = []

    for x in difficultiesC:

        board_base = generate(x, 10)

        board = board_base.board
        solution = board_base.solve().board

        flattened_board = flatten_join(board)
        flattened_solution = flatten_join(solution)

        boardDict = {'grid': flattened_board,
                         'solution': flattened_solution,
                         'difficulty': x}


        boards.append(boardDict)





    # Add the users into the model
    for userData in users:
            u = User.objects.get_or_create(username=userData['username'], email=userData['email'])[0]
            u.password = userData['password']
            u.save()
            print(u)

    # Add boards in to the model for easy, medium and hard difficulty
    for boardData in boards:

        b = addBoards(boardData['grid'], boardData['solution'], boardData['difficulty'], None)

        print(b)
        counter = 0
        scoreCounter = 0

        for user in users:
            username = User.objects.get_by_natural_key(user.get('username'))

            # The scores are added based on different difficulties.
            if b.difficulty == 'M':
                g = addGame(b, username, scoreMedium[scoreCounter], dates[counter])
            elif b.difficulty == 'E':
                g = addGame(b, username, scoreEasy[scoreCounter], dates[counter])
            elif b.difficulty == 'H':
                g = addGame(b, username, scoreHard[scoreCounter], dates[counter])

            counter += 1
            scoreCounter += 1
            if counter > 3:
                counter = 0
            if scoreCounter > 13:
                scoreCounter = 0
            print(g)


    # create new board for daily challenge
    board_base = generate('M', 11)

    board = board_base.board
    solution = board_base.solve().board

    flattened_board = flatten_join(board)
    flattened_solution = flatten_join(solution)
    b = addBoards(flattened_board, flattened_solution, None, date)
    print(b)
    for user in users:
        username = User.objects.get_by_natural_key(user.get('username'))
        g = addGame(b, username, scoreDC[scoreCounter], dates[counter])
        scoreCounter +=1
        counter+=1
        if counter > 3:
            counter = 0
        if scoreCounter > 13:
            scoreCounter = 0
        print (g)



def addBoards(grid, solution, difficulty, postedDate):
    b = Board.objects.get_or_create(grid=grid, solution=solution, difficulty=difficulty,postedDate=postedDate )[0]
    b.save()
    return b




def addGame(b, user, score, date):
    g = Game.objects.get_or_create(board=b, user=user, score=score, submissionDate= date)[0]
    g.save()
    return g


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
