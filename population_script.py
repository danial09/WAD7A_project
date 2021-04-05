import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD7A_project.settings')

import django

django.setup()

from sudokugame.models import Board, Game
from sudokugame.sudoku_core import generate, flatten_join, solve, get_flattened_info, generate_score
from django.utils import timezone
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta

from sudokugame.views import create_board, create_daily_challenge

def populate():
    # Ensure results can be replicated
    random.seed(10)

    # List of dictionaries containing data belonging to a model

    # Create 14 usernames to test with

    names = ['Yuh31Ku4ui', 'K0taM0r1n15h1', 'KenEnd0', 'Da1Tantan', 'BastianV1alJa1m3', 'T11tVunk', 'J1nC3',
             'JanMr0z05k1', 'H1d3ak1J0', 'Jakub0ndr0us3k', 'Th0ma35nyd3r', 'RobertBab10n', 'Brank0C3raIc', 'JanaTyl0va']

    users = [{'username': name, 'email': f'{name}@test.com', 'password': 'testPassword'} for name in names]

    # Add the users into the model
    users_list = []  # To store the created users to be used afterwards
    for userData in users:
        u, c = User.objects.get_or_create(username=userData['username'], email=userData['email'])
        if c:
            u.set_password(userData['password'])
        u.save()
        users_list.append(u)
        print(f'Made user {u.username}')

    # Generate 75 games for normal boards, each with a submission date 4 hours before the other,
    # starting from the current time. This will allow us the check the time limit filter in the leaderboards.
    print("Generating normal games")
    time = timezone.now()
    for i in range(75):
        difficulty = random.choice("EMH") # Difficulty between Easy, Medium, Hard
        user = random.choice(users_list)
        board = create_board(difficulty)  # Use create_board from sudokugame app as it's simpler
        if bool(board_query := Board.objects.filter(grid=board.grid)):
            board = board_query[0]
        else:
            board.save()

        print(f"Created board {board}")
        simulate_game(board, user, time)
        time -= relativedelta(hours=4)

    # Generate results for a daily challenge game
    # For first 7 users, generate a result of zero, this should prevent them from partaking in the challenge for today
    # but should also not show up in the leaderboard
    challenge_board = create_daily_challenge()
    print("Generating failed daily challenge attempts")
    for i in range(0, 7):
        addGame(challenge_board, user=users_list[i], score=0, date=timezone.now())
        print(f"")

    # For the remaining seven, let's just simulate a normal game
    print("Generating successful daily challenge attempts")
    for i in range(7, 14):
        simulate_game(board=challenge_board, user=users_list[i], submission_date=timezone.now())


    # Generate empty results, these should not be shown in the database
def simulate_game(board, user, submission_date):
    time_taken = random.randint(50, 20 * 60)  # Number of seconds user took for game
    score = generate_score(time_taken, random.randint(0, 3), random.randint(1, 3))
    game = addGame(board, user, score, submission_date)
    print(game)

def addGame(b, user, score, date):
    g = Game(board=b, user=user, score=score, submissionDate=date)
    # If a game with this board and user has already been created, then let us remake it
    if bool(gameCheck := Game.objects.filter(board=b, user=user)):
        g = gameCheck[0]
    else:
        g = Game(board=b, user=user)

    g.score = score
    g.submissionDate = date
    g.save()

    return g


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
