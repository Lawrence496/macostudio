from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name='signout'),
    path('profile', views.profile, name='profile'),
    path('check_username/', views.check_username, name='check_username'),
    path('select-genres/', views.genre_selection, name='genre_selection'),
]
