import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD7A_project.settings')

import django

django.setup()

from sudokugame.models import Board, Game
from sudokugame.sudoku_core import generate, flatten_join, solve
from django.utils import timezone
from django.contrib.auth.models import User


def populate():
    # List of dictionaries containing data belonging to a model

    # Random username and scores
    users = [
        {1011: {'username': 'TestUsername1',
         'email': 'testusername1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {2600:{'username': 'TestUsername2',
         'email': 'testusername2@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {3300:{'username': 'TestUsername3',
         'email': 'testusername3@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {4300:{'username': 'TestUsername4',
         'email': 'testusername4@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {5600:{'username': 'TestUsername5',
         'email': 'testusername5@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {6040:{'username': 'TestUsername6',
         'email': 'testusername7@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {7600:{'username': 'TestUsername8',
         'email': 'testusername1@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
         {8500:{'username': 'TestUsername9',
         'email': 'testusername9@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'}},
        {500:{'username': 'TestUsername10',
         'email': 'testusername10@test.com',
         'password': 'TtEeSsTtPpAaSsWwOoRrDd123'} },
    ]
    # Create actual users
    # save them
    # user django.models to import user and use actual users instances to put in game object

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

    # mdate = datetime.date(2021,4,4)
    date = timezone.now()

    # Add the users into the model
    for userData in users:
        for score, user in userData.items():
            u = User.objects.get_or_create(username=user['username'], email=user['email'])[0]
            u.password = user['password']
            u.save()
            print(u)

    # Add boards in to the model
    for boardData in boards:
        b = addBoards(boardData['grid'], boardData['solution'], boardData['difficulty'])
        print (b)
        for userData in users:
            for score, user in userData.items():
                username = User.objects.get_by_natural_key(user.get('username'))
                g = addGame(b, username, score, date)
                print(g)


#
#     # print out the games we have added
#     for b in Board.objects.all():
#         for g in Game.objects.filter(id=b['id']):
#             print(f'- {b}: {g}')
#
#         # Function to add boards of different boards to the model
#
#
def addBoards(grid, solution, difficulty):
    b = Board.objects.get_or_create(grid=grid, solution=solution, difficulty=difficulty)[0]
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
