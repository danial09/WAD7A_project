import sys

from random import randrange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import time

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from sudokugame.forms import UserForm
from sudokugame.models import Game, Board

from sudokugame.sudoku_core import generate, flatten_join, difficulties, get_flattened_info, generate_score


def home(request):
    if request.user.is_authenticated:
        challenge_done = Game.objects.filter(user=request.user).filter(board__postedDate=timezone.now().date()).exists()
    else:
        challenge_done = False

    return render(request, 'sudokugame/home.html', context={'challenge_done': challenge_done})


def create_daily_challenge():
    board_check = Board.objects.filter(postedDate=timezone.now().date())
    if bool(board_check):
        return board_check[0]

    grid, solution = get_flattened_info(generate('M'))
    board = Board(grid=grid, solution=solution, postedDate=timezone.now().date())
    board.save()
    return board


def create_board(difficulty):
    # Sanity check to make sure difficulty passed does in fact exist.
    difficulty = difficulty if difficulty in difficulties else 'M'

    grid, solution = get_flattened_info(generate(difficulty))
    return Board(grid=grid, solution=solution, difficulty=difficulty)


def start_game(request, board):
    if board.is_daily_challenge_board():
        request.session['board_id'] = board.id
    else:
        request.session['board'] = board.grid

    request.session['solution'] = board.solution
    request.session['difficulty'] = board.difficulty
    request.session['start_time'] = int(time())
    request.session['lives'] = 3
    request.session['hints'] = 3
    request.session['remaining'] = sum([1 if x == '0' else 0 for x in board.grid])

def add_game(request):
    time_taken = (int(time()) - request.session['start_time'])

    score = generate_score(time_taken, request.session['hints'], request.session['lives'])
    if 'board_id' in request.session:
        board = Board.objects.filter(id=request.session['board_id'])[0]
    else:
        board = Board(grid=request.session['board'], solution=request.session['solution'], difficulty=request.session['difficulty'])
        board.save()

    # Don't add game if the user has already played this board.
    if Game.objects.filter(board=board).filter(user=request.user).exists():
        return

    game = Game(board=board, user=request.user, score=score, submissionDate=timezone.now())
    game.save()


def add_failed_daily_challenge(request):
    board = Board.objects.filter(id=request.session['board_id'])[0]
    game = Game(board=board, user=request.user, score=0, submissionDate=timezone.now())
    game.save()

def stop_game(request):
    if 'board_id' in request.session:
        del request.session['board_id']
    else:
        del request.session['board']
        del request.session['solution']
        del request.session['difficulty']

    del request.session['start_time']
    del request.session['lives']
    del request.session['hints']


def play(request):
    board = create_board(request.GET.get("difficulty"))
    start_game(request, board)

    return render(request, 'sudokugame/play.html', context={'board': board})

def practice(request):
    board = create_board('M')
    return render(request, 'sudokugame/practice.html', context={'board': board})


@login_required
def dailychallenge(request):
    if Game.objects.filter(user=request.user).filter(board__postedDate=timezone.now().date()).exists():
        return redirect(reverse('sudokugame:home'))

    board = create_daily_challenge()
    start_game(request, board)
    return render(request, 'sudokugame/dailychallenge.html', context={'board': board})

# Create a registration view
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # hash the password with the set_password method
            # then update the user object. 
            user.set_password(user.password)
            user.save()
            return redirect(reverse('sudokugame:login'))
        else:
            print(user_form.errors)
    else:
        # The request is not 'POST', we render our form. Its ready for user input. 
        user_form = UserForm()

    return render(request, 'sudokugame/register.html', context={'user_form': user_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("sudokugame:home"))

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse("sudokugame:home"))
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'sudokugame/login.html', context={'user_form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('sudokugame:home'))

@login_required
def profile_page(request):
    current_user = request.user
    queryset = Game.objects.filter(user=current_user).order_by("-score")[:5]

    return render(request, "sudokugame/profile.html", {'games': queryset})

def leader_board(request):
    return render(request, "sudokugame/leaderboard.html")


def help_page(request):
    flattened_board = flatten_join(generate("M").board)
    board = Board(grid=flattened_board)
    return render(request, "sudokugame/help.html", context={"example_board": board})


def ajax_solve(request, _):
    solution = request.session['solution']
    stop_game(request)

    return JsonResponse({'solution': solution})


def ajax_hint(request, _):
    if request.session['hints'] > 0:
        row = request.GET.get('row')
        col = request.GET.get('col')

        solution = request.session['solution']
        value = solution[9*int(row) + int(col)]

        request.session['hints'] -= 1
    else:
        value = 0

    return JsonResponse({'value': value})


def ajax_input(request, _):
    row = request.GET.get('row')
    col = request.GET.get('col')
    val = request.GET.get('val')

    return_json = {}

    solution = request.session['solution']
    solution_val = solution[9*int(row) + int(col)]

    if val == solution_val:
        result = "correct"
        request.session["remaining"] -= 1
        if request.session["remaining"] == 0:
            if request.user.is_authenticated():
                add_game(request)
            stop_game(request)
    else:
        result = "incorrect"
        request.session['lives'] -= 1
        if request.session['lives'] == 0:
            if 'board_id' in request.session and request.user.is_authenticated():
                add_failed_daily_challenge(request)
            stop_game(request)
            return_json['solution'] = solution

    return_json['result'] = result
    return JsonResponse(return_json)

def ajax_leaderboard(request):
    time = timezone.now()
    time_limit = request.GET.get("timeLimit", 'month')
    board_type = request.GET.get("boardType", 'M')
    if time_limit == 'day':
        time -= relativedelta(days=1)
    elif time_limit == 'week':
        time -= relativedelta(weeks=1)
    else:
        time -= relativedelta(months=1)

    queryset = Game.objects.filter(submissionDate__gt=time)

    if board_type != "DC":
        queryset = queryset.filter(board__difficulty=board_type)
    else:
        queryset = queryset.filter(board__postedDate=timezone.now().date()).filter(score__gt=0)

    queryset = queryset.order_by("-score")[:10]

    data = [{'username': game.user.username, 'score': game.score} for game in queryset]

    response = JsonResponse(data, safe=False)
    return response
