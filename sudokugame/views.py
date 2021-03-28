import sys
from random import randrange

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from sudoku import Sudoku

from sudokugame.forms import UserForm


# Create your views here.

def test(request):
    puzzle = Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(0.7)
    flattened = [str(cell) if cell is not None else '0' for row in puzzle.board for cell in row]

    return render(request, 'sudokugame/test.html', context={'board': flattened})

def home(request):
    context_dict = {}

    return render(request, 'sudokugame/home.html', context=context_dict)


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
