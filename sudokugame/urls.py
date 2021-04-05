from django.urls import path, re_path
from sudokugame import views
from django.urls import reverse

app_name = "sudokugame"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('play/', views.play, name='play'),
    path('logout/', views.user_logout, name='logout'),
    path('leaderboard/', views.leader_board, name='leaderboard'),
    path('profile/', views.profile_page, name='profilepage'),
    path('help/', views.help_page, name='help'),
    path('practice/', views.practice, name='practice'),
    path('dailychallenge/', views.dailychallenge, name='dailychallenge'),
    path('leaderboard/ajax/get/', views.ajax_leaderboard),
    re_path(r'^(play|dailychallenge)/ajax/solve/$', views.ajax_solve),
    re_path(r'^(play|dailychallenge)/ajax/hint/$', views.ajax_hint),
    re_path(r'^(play|dailychallenge)/ajax/input/$', views.ajax_input),
]
