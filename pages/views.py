from django.shortcuts import render
from movies.models import Movies, UserGenrePreference, Series
from django.db.models import Q

# Create your views here.
def get_user_preferences(user):
    try:
        preference = UserGenrePreference.objects.get(user=user)
        preferred_genres = preference.genres.all() 
        return preferred_genres
    except UserGenrePreference.DoesNotExist:
        return []  

def get_movies_by_genres(genres):
    return Movies.objects.filter(categories__in=genres).distinct() 

def get_series_by_genres(series_genre_ids):
    for series in Series.objects.all():
        series_genre_ids = [genre.id for genre in series.categories.all()]
    
    series = Series.objects.filter(categories__in=series_genre_ids).distinct()
    return series

def recommend_series_for_user(user):
    preferred_genres = get_user_preferences(user)
    
    if not preferred_genres:
        return Series.objects.none()  
    
    recommended_series = get_series_by_genres(preferred_genres).order_by('-first_air_date','-rating')
    return recommended_series

def recommend_movies_for_user(user):
    preferred_genres = get_user_preferences(user)
    
    if not preferred_genres:
        return Movies.objects.none()  
    
    recommended_movies = get_movies_by_genres(preferred_genres).order_by('-release_date','-rating')
    return recommended_movies

def index(request):
    best_rated = Movies.objects.order_by('-rating')[:10]
    latest_movies = Movies.objects.order_by('-release_date')[:6]
    movies = Movies.objects.filter(movie_categories__iexact='Movie')[:12]
    tv_series = Series.objects.all()[:12]
    cartoons = Movies.objects.filter(movie_categories__iexact='Cartoon')[:12]
    
    latest_tv_series = Series.objects.all().order_by('-rating', '-first_air_date')[:6]
    
    if request.user.is_authenticated:
        recommended_movies = recommend_movies_for_user(request.user)[:6]
        recommended_series = recommend_series_for_user(request.user)[:6]
    else:
        recommended_movies = Movies.objects.all()[:6]
        recommended_series = Series.objects.all().order_by('-rating')[:6]
        
    data = {
        'best_rated': best_rated,
        'latest_movies': latest_movies,
        'movies': movies,
        'tv_series': tv_series,
        'cartoons': cartoons,
        'recommended_movies': recommended_movies,
        'recommended_series': recommended_series,
        'latest_tv_series': latest_tv_series,
    }
    
    return render(request, 'index.html', data)

def about(request):
    return render(request, 'pages/about.html')

def faq(request):
    return render(request, 'pages/faq.html')

def pricing(request):
    return render(request, 'pages/pricing.html')