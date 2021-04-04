from django.urls import path
from sudokugame import views

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
    path('leaderboard/ajax/leaderboardGet/', views.ajax_leaderboard),
]
