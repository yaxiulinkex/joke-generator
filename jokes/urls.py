from django.urls import path
from . import views

app_name = 'jokes'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.joke_history, name='history'),
    path('api/random/', views.get_random_joke_api, name='api_random'),
    path('type/<str:joke_type>/', views.joke_by_type, name='by_type'),
]
