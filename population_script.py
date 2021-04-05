import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD7A_project.settings')

import django

django.setup()

from sudokugame.models import Board, Game
from sudokugame.sudoku_core import generate, flatten_join, generate_score
from django.utils import timezone
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
import random



def populate():
    # List of dictionaries containing data belonging to a model

    # Random username and scores
    users = [
        {'username': 'Yuh31Ku4ui',
         'email': 'Yuh31Ku4ui@test.com',
         'password': 'TtEeS'},
        {'username': 'K0taM0r1n15h1',
         'email': 'K0taM0r1n15h1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'KenEnd0',
         'email': 'KenEnd0@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'Da1Tantan',
         'email': 'Da1Tantan@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'BastianV1alJa1m3',
         'email': 'BastianV1alJa1m3@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'T11tVunk',
         'email': 'T11tVunk@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'J1nC3',
         'email': 'J1nC3@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
         {'username': 'JanMr0z05k1',
         'email': 'JanMr0z05k1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'H1d3ak1J0',
         'email': 'H1d3ak1J0@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'Jakub0ndr0us3k',
         'email': 'Jakub0ndr0us3k@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'Th0ma35nyd3r',
         'email': 'Th0ma35nyd3r@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'RobertBab10n',
         'email': 'RobertBab10n@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'Brank0C3raIc',
         'email': 'Brank0C3raIc14@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
        {'username': 'JanaTyl0va',
         'email': 'JanaTyl0va@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'},
    ]
    scoreEasy = []
    scoreMedium = []
    scoreHard = []
    scoreDC = []

    for x in range(15):
        scoreEasy.append(generate_score(random.randint(180,4500), 1, 1))
        scoreMedium.append(generate_score(random.randint(180,4500), 1, 1))
        scoreHard.append(generate_score(random.randint(180,4500), 1, 1))
        scoreDC.append(generate_score(random.randint(180,4500), 1, 1))

    print (scoreMedium)


    # different dates to test teh daily, weekly and monthly leaderboard
    date = timezone.now()
    dates = [date, date - relativedelta(days=1), date - relativedelta(weeks=1), date - relativedelta(months=1) -
             relativedelta(days=2)]
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
