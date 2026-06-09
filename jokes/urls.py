from django.urls import path
from . import views

app_name = 'jokes'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Jokes
    path('jokes/', views.index, name='jokes_index'),
    path('jokes/history/', views.joke_history, name='joke_history'),
    path('jokes/type/<str:joke_type>/', views.joke_by_type, name='joke_by_type'),
    path('api/joke/random/', views.get_random_joke_api, name='api_random_joke'),
    
    # Games
    path('games/', views.games, name='games'),
    path('games/<str:game_id>/', views.game_detail, name='game_detail'),
    path('games/leaderboard/', views.game_leaderboard, name='game_leaderboard'),
    path('api/game/score/', views.save_game_score, name='save_game_score'),
    
    # Photos
    path('photos/', views.photos, name='photos'),
    path('api/photo/random/', views.get_random_photo_api, name='api_random_photo'),
    
    # Productivity
    path('productivity/', views.productivity_hub, name='productivity'),
    path('api/tip/random/', views.get_random_tip_api, name='api_random_tip'),
]
