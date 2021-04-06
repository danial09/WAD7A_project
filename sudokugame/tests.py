from django.test import TestCase
import os
import re
from sudokugame import forms
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