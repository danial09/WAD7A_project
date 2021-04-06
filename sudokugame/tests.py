from django.test import TestCase
import os
import re
import random
from sudokugame import forms
from sudokugame import views
from sudokugame.sudoku_core import generate_score
from sudokugame.models import Game 
from django.urls import reverse
from django.conf import settings
from django.forms import fields as django_fields
from django.contrib.auth.models import User


# The template has been adapted from rango test cases

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

# Test the database

# Does the git ignore contain database
class DatabaseTests(TestCase):
    def setUp(self):
        pass

    def gitignore_setup_check(self,path):
        file = open(path, 'r')

        for f in file:
            f = f.strip()
            if f.startswith('db.sqlite3'):
                return True
        f.close()
        return False

    def test_gitignore_setup(self):
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        gitignore_path = os.path.join(git_base_dir, '.gitignore')

        if os.path.exists(gitignore_path):
            self.assertTrue(self.gitignore_setup_check(gitignore_path), f"{FAILURE_HEADER} .gitignore file does not inclue 'db.sqlite3'")
        else:
            warnings.warn(".gitignore file was not found in the repository")


# Helper function
def create_user():
    user = User.objects.get_or_create(username='testuser',
                                      email='testuser@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

def get_template(path):
    file = open(path, 'r')
    template_str = ''

    for line in file:
        template_str = f'{template_str}{line}'
    file.close()
    return template_str

#Please check if this is right UK
def remove_zeros_from_board(grid_str):

    stripped_grid_str = ""
    for character in grid_str:
        if character != "0":
            stripped_grid_str = stripped_grid_str + character
    
    return stripped_grid_str


class RegistrationFormTests(TestCase):

    def test_user_form(self):

        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER} User form was not found in forms.py{FAILURE_FOOTER}")

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f'{FAILURE_HEADER}The userfrom doesnot match user model{FAILURE_FOOTER}')

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for e in expected_fields:
            expected_field= expected_fields[e]

            self.assertTrue(e in fields.keys(), f"{FAILURE_HEADER}{e} was not found in User Form{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[e]), f"{FAILURE_HEADER}{e} does not match the correct type.Expected {expected_field} got {type(fields[e])}{FAILURE_FOOTER}")

class RegistrationTests(TestCase):
    def test_registration_view_exists(self):
        url = ''
        try:
            url = reverse('sudokugame:register')
        except:
            pass

        self.assertEqual(url, '/register/', f"{FAILURE_HEADER}Url for registration has not been mapped correctly{FAILURE_FOOTER}")


    def test_registration_template(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'sudokugame')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path),f"register.html was not found in templates/sudokugame")

        template_str = get_template(template_path)
        title_pattern = r'<title>(\s*|\n*)Register(\s*|\n*)</title'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('sudokugame:register'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(title_pattern, content), f"{FAILURE_HEADER}The title is not correct{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str),f"{FAILURE_HEADER}Template inheritance has not been used{FAILURE_FOOTER}")


    def test_registration_form_inaction(self):
        user_data = {'username':'testuser',
                    'email':'testuser@test.com',
                     'password':'test123'}
        user_form = forms.UserForm(data=user_data)

        self.assertTrue(user_form.is_valid(),f"{FAILURE_HEADER}The user form was not valid after entering valid data{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()

        self.assertTrue(User.objects.get_by_natural_key('testuser'), f"{FAILURE_HEADER}The user object was not created properly{FAILURE_FOOTER}")


class LoginTests(TestCase):
    def test_login_view_exists(self):
        url = ''
        try:
            url = reverse('sudokugame:login')
        except:
            pass

        self.assertEqual(url, '/login/', f"{FAILURE_HEADER}Url for registration has not been mapped correctly{FAILURE_FOOTER}")

    def test_login_template(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'sudokugame')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path),f"login.html was not found in templates/sudokugame")

        template_str = get_template(template_path)
        title_pattern = r'<title>(\s*|\n*)Login(\s*|\n*)</title'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('sudokugame:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(title_pattern, content), f"{FAILURE_HEADER}The title is not correct{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str),f"{FAILURE_HEADER}Template inheritance has not been used{FAILURE_FOOTER}")



    def test_login_functionality(self):
       user_object = create_user()

       response = self.client.post(reverse('sudokugame:login'), {'username': 'testuser', 'password':'testabc123'})

       try:
           self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Attempt to login with if of {user_object} but failed{FAILURE_FOOTER}")
       except:
           self.assertTrue(False, f'{FAILURE_HEADER}The login() view did not log in as expected{FAILURE_FOOTER}')

       self.assertEqual(response.status_code,302,f"{FAILURE_HEADER}The login page was not redirected after successful login{FAILURE_HEADER}")
       self.assertEqual(response.url, reverse('sudokugame:home'),f"{FAILURE_HEADER}Redirected to wrong page other than home{FAILURE_FOOTER}")

class LogoutTests(TestCase):

    def test_logout_without_login(self):
        response = self.client.get(reverse('sudokugame:logout'))
        self.assertTrue(response.status_code,302)
        self.assertTrue(response.url, reverse('sudokugame:login'))

    def test_logout_with_login(self):
        user_object = create_user()
        self.client.login(username = 'testuser', password= 'testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Login attempt failed{FAILURE_FOOTER}")
        except:
            self.assertTrue(False, f"{FAILURE_HEADER}Login attempt failed. Please check you login() view{FAILURE_FOOTER}")

        response = self.client.get(reverse('sudokugame:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Redirection failed after logging out a user{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('sudokugame:home'), f"{FAILURE_HEADER}Redirected to wrong page{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logout failed{FAILURE_FOOTER}") 

#untested, don't know if these work, please check before merging UK

class BoardModelTests(TestCase):

    def set_up(self):

        boardE = create_board("E")
        boardE.save()

        boardM = create_board("M")
        boardM.save()

        boardH = create_board("H")
        boardH.save()

        boardDC = create_daily_challenge()

    def test_grid_length(self):

        self.assertTrue(boardE.grid.length()==81, f"{FAILURE_HEADER}Easy grid isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardM.grid.length()==81, f"{FAILURE_HEADER}Medium grid isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardH.grid.length()==81, f"{FAILURE_HEADER}Hard grid isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardDC.grid.length()==81, f"{FAILURE_HEADER}Daily Challenge grid isn't the right size{FAILURE_FOOTER}")

    def test_solution_length(self):

        self.assertTrue(boardE.solution.length()==81, f"{FAILURE_HEADER}Easy solution isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardM.solution.length()==81, f"{FAILURE_HEADER}Medium solution isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardH.solution.length()==81, f"{FAILURE_HEADER}Hard solution isn't the right size{FAILURE_FOOTER}")
        self.assertTrue(boardDC.solution.length()==81, f"{FAILURE_HEADER}Daily Challenge solution isn't the right size{FAILURE_FOOTER}")

    def test_daily_challenge_postedDate(self):

        self.assertEqual(boardDc.postedDate, timezone.now().date(), f"{FAILURE_HEADER}The DC doesnt have today's date{FAILURE_FOOTER}")

    def test_normalboard_difficulty(self):

        self.assertEqual(boardE.difficulty, 'E', f"{FAILURE_HEADER}Easy board doesn't have easy difficulty{FAILURE_FOOTER}")
        self.assertEqual(boardM.difficulty, 'M', f"{FAILURE_HEADER}Medium board doesn't have medium difficulty{FAILURE_FOOTER}")
        self.assertEqual(boardH.difficulty, 'H', f"{FAILURE_HEADER}Hard board doesn't have hard difficulty{FAILURE_FOOTER}")

    def test_difficulty_fill(self):

        self.assertEqual(remove_zeros_from_board(boardE.grid).length(), 37, f"{FAILURE_HEADER}Easy board doesn't have the right number of filled cells{FAILURE_FOOTER}")
        self.assertEqual(remove_zeros_from_board(boardM.grid).length(), 27, f"{FAILURE_HEADER}Easy board doesn't have the right number of filled cells{FAILURE_FOOTER}")
        self.assertEqual(remove_zeros_from_board(boardH.grid).length(), 17, f"{FAILURE_HEADER}Easy board doesn't have the right number of filled cells{FAILURE_FOOTER}")


class GenerateScoreTests(TestCase):

    def test_generate_score:

        time_taken = random.randint(0, 15)
        hints = random.randint(0, 3)
        lives = random.randint(0, 3)

        score = 50 + (max(15-time_taken, 0))*20

        if hints == 3:
            score += 100

        if lives == 3:
            score += 100


        self.assertEqual(generate_score(time_taken*60, hints, lives), score, f"{FAILURE_HEADER}Generate score isn't working right{FAILURE_FOOTER}")

    def test_generate_score_range(self):

        time_taken = random.randint(0, 15)*60
        hints = random.randint(0, 3)
        lives = random.randint(0, 3)
        score = generate_score(time_taken, hints, lives)

        self.assertTrue(score <= 550 and score >= 50, f"{FAILURE_HEADER}Generate score isn't generating in range{FAILURE_FOOTER}")
