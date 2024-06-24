from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieView, name='movies'),
    path('search', views.MovieSearch, name='search'),
    path('log_video_watch/', views.log_video_watch, name='log_video_watch'),
    path('<int:id>', views.MovieDetails, name='movie-details'),
    path('series', views.SeriesView, name='series'),
    path('cartoon', views.CartoonView, name='cartoons'),
    path('series/<int:id>', views.SeriesDetails, name='series-details'),
]
