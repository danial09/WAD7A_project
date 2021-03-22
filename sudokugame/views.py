import sys
from random import randrange

from django.shortcuts import render

from sudoku import Sudoku

from sudokugame.forms import UserForm


# Create your views here.

def test(request):
    puzzle = Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(0.7)
    flattened = [str(cell) if cell is not None else '0' for row in puzzle.board for cell in row]

    return render(request, 'sudokugame/test.html', context={'board': flattened})


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
            print  (user_form.errors)
    else:
        # The request is not 'POST', we render our form. Its ready for user input. 
        user_form = UserForm()        
    
    return render(request, 'sudokugame/register.html', context = {'user_form': user_form, 'registered': registered})
