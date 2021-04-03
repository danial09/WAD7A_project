import sys
from random import randrange

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from sudoku import Sudoku

from sudokugame.forms import UserForm
from sudokugame.models import Game, Board

from sudokugame.sudoku_core import generate, flatten_join, difficulties


def home(request):
    return render(request, 'sudokugame/home.html')


def create_board(request):
    board_id = request.GET.get('id')
    if board_id is not None:
        return get_object_or_404(Board, pk=board_id)

    difficulty = request.GET.get('difficulty', 'M')
    # Sanity check to make sure difficulty passed does in fact exist.
    difficulty = difficulty if difficulty in difficulties else 'M'
    board_base = generate(difficulty)
    board = board_base.board
    solution = board_base.solve().board

    flattened_board = flatten_join(board)
    flattened_solution = flatten_join(solution)

    board = Board.objects.filter(grid=flattened_board)
    if bool(board):
        return board[0]
    else:
        board = Board(grid=flattened_board, solution=flattened_solution, difficulty=difficulty)
        board.save()
        return board


def play(request):
    board = create_board(request)

    return render(request, 'sudokugame/play.html', context={'board': board})


# Create a registration view
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # hash the password with the set_password method
            # then update the user object. 
            user.set_password(user.password)
            user.save()
            registered =True
        else:
            print(user_form.errors)
    else:
        # The request is not 'POST', we render our form. Its ready for user input. 
        user_form = UserForm()

    return render(request, 'sudokugame/register.html', context={'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # Redirects to the Home page
                return redirect(reverse("sudokugame:home"))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, "sudokugame/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('sudokugame:home'))

@login_required
def profile_page(request):

    current_user = request.user
    queryset = Game.objects.filter(user = current_user).order_by("-score")[:10]

    context = {"users_games": queryset, "user": current_user}

    return render(request, "sudokugame/profile.html", context)

def leader_board(request):

    querysetE = Game.objects.filter(board__difficulty = "E").order_by("-score")[:10]
    querysetM = Game.objects.filter(board__difficulty = "M").order_by("-score")[:10]
    querysetH = Game.objects.filter(board__difficulty = "H").order_by("-score")[:10]
    querysetDCTemp = Game.objects.filter(board__postedDate__isnull = False)
    querysetDC = querysetDCTemp.order_by("board__postedDate").order_by("-score")[:10]

    context = {"Easygamelist": querysetE, "Mediumgamelist": querysetM, "Hardgamelist": querysetH, "Dailychallengelist": querysetDC}

    return render(request, "sudokugame/leaderboard.html", context)



