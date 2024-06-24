from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from movies.models import Movies, Category, Reviews, VideoWatch, MovieInteraction, Series, Episode
from movies.serializer import MovieSerializer
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import requests
import json
from django.contrib.auth.models import User

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    
def MovieView(request):
    latest_movies = Movies.objects.order_by('-release_date')[:6]
    movies = Movies.objects.filter(movie_categories__iexact='Movie').order_by('-release_date')
    tv_series = Movies.objects.filter(movie_categories='movie_categories')
    get_all_category = Category.objects.all()
    movie_categories = Movies.objects.values_list('movie_categories', flat=True).distinct()
    
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    data = {
        'latest_movies': latest_movies,
        'movies': movies,
        'tv_series': tv_series,
        'all_category': get_all_category,
        'movie_categories': movie_categories,
        'page': page,
    }
    
    return render(request, 'movies/movie.html', data)

def SeriesView(request):
    series = Series.objects.order_by('-first_air_date')
    paginator = Paginator(series, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    data = {
        'series': series,
        'page': page,
    }
    return render(request, 'movies/series.html', data)

def CartoonView(request):
    cartoon = Movies.objects.filter(movie_categories__iexact='Cartoon')
    
    paginator = Paginator(cartoon, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'cartoons': cartoon,
        'page': page,
    }
    
    return render(request, 'movies/cartoon.html', data)

def MovieSearch(request):
    query = request.GET.get('query')
    
    if query:
        movies = Movies.objects.filter(Q(title__icontains=query)).distinct()[:12]
        series = Series.objects.filter(Q(title__icontains=query)).distinct()[:12]

        data = {
            'movies': movies,
            'series': series,
            'query': query,
        }
        return render(request, 'movies/search.html', data)
    else:
        return render(request, 'movies/search.html', {'query': query})
    

def recommend_movies(movie):
        genre = movie.categories.all()
        release_year = movie.release_date.year
        categories = movie.movie_categories
        rating = movie.rating
        
        recommended_movies = Movies.objects.filter(
            Q(categories__in=genre) &
            Q(rating__gte=rating-2, rating__lte=rating+2) & Q(movie_categories__iexact=categories)
        ).exclude(id=movie.id)[:6]
        
        return recommended_movies

def recommend_series(series):
    genre = series.categories.all()
    rating = series.rating
    
    if rating is not None:
        recommended_series = Series.objects.filter(Q(rating__gte=rating-2, rating__lte=rating+2) & Q(categories__in=genre)).exclude(id=series.id)[:6]
    else:
        recommended_series = Series.objects.filter(categories__in=genre).exclude(id=series.id)[:6]
    
    return recommended_series

@login_required
def log_video_watch(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            movie_id = data.get('movie_id')

            if not movie_id:
                return JsonResponse({'status': 'error', 'message': 'No movie ID provided'}, status=400)

            movie = Movies.objects.get(id=movie_id)

            # Check if the user has already watched this movie
            if not VideoWatch.objects.filter(user=request.user, movie=movie).exists():
                VideoWatch.objects.create(user=request.user, movie=movie)

            return JsonResponse({'status': 'success', 'message': 'Playback logged'})
        except Movies.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Movie not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required
def log_movie_interaction(request, id):
    if request.method == 'GET':
        user = request.user
        action = 'watched'  
        # Retrieve the movie object using the provided movie_id
        try:
            movie = get_object_or_404(Movies, pk=id)
        except Movies.DoesNotExist:
            return HttpResponse('Movie not found.', status=404)

        # Save the interaction in the database
        interaction = MovieInteraction.objects.create(user=user, movie=movie, action=action)
        interaction.save()

        return HttpResponse('Movie watched interaction logged successfully.')
    else:
        return HttpResponse('Only POST requests are allowed.', status=405)

    
@login_required
def MovieDetails(request, id):
    movie_details = get_object_or_404(Movies, pk=id)
    
    if request.method == "POST":
        title = request.POST.get('title')
        review = request.POST.get('review')
        rating = float(request.POST.get('rating', 0.0))
        
        reviews = Reviews.objects.create(movie=movie_details, user=request.user, title=title, review=review, rating=rating)
      
        return redirect('movie-details', id=id)

    recommended_movies = recommend_movies(movie_details)

    reviews = Reviews.objects.filter(movie=movie_details).order_by('-created_at')[:3]
    
    data = {
        'reviews': reviews,
        'movie_details': movie_details,
        'recommended_movies': recommended_movies,
    }
    
    return render(request, 'movies/movie-details.html', data)

@login_required
def SeriesDetails(request, id):
    series_detail = get_object_or_404(Series, pk=id)
    
    if request.method == "POST":
        title = request.POST.get('title')
        review = request.POST.get('review')
        rating = float(request.POST.get('rating', 0.0))
        
        reviews = Reviews.objects.create(series=series_detail, user=request.user, title=title, review=review, rating=rating)
      
        return redirect('series-details', id=id)

    recommended_series = recommend_series(series_detail)
    
    reviews = Reviews.objects.filter(series=series_detail).order_by('-created_at')[:3]
    
    episodes = series_detail.episodes.all().order_by('season_number', 'episode_number')
    
    seasons = {}
    for episode in episodes:
        if episode.season_number not in seasons:
            seasons[episode.season_number] = []
        seasons[episode.season_number].append(episode)
        
    sorted_seasons = sorted(seasons.items())
    print(sorted_seasons)

    data = {
        'recommended_series': recommended_series,
        'reviews': reviews,
        'series_detail': series_detail,
        'sorted_seasons':sorted_seasons,
    }
    
    return render(request, 'movies/series-details.html', data)
    