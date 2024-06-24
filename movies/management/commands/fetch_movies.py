from django.core.management.base import BaseCommand
from movies.models import Movies, Category
from movies.api import fetch_movies, fetch_tv_series, fetch_cartoon_movies
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches and stores movies and their categories from the TMDb API'

    def handle(self, *args, **kwargs):
        api_key = '2af8f53d7614f389368f9ee77ab3d464'
        
        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None
        
        genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
        genres_response = requests.get(genres_url)
        genres_data = genres_response.json().get('genres', [])
        genres_dict = {genre['id']: genre['name'] for genre in genres_data}
        
        def get_or_create_categories(genre_ids):
            category_objects = []
            for genre_id in genre_ids:
                genre_name = genres_dict.get(genre_id)
                if genre_name:
                    category, created = Category.objects.get_or_create(category=genre_name)
                    category_objects.append(category)
            return category_objects

        movies_data = fetch_movies(api_key, 'Planet')
        for movie_data in movies_data['results']:
            release_date = parse_date(movie_data.get('release_date', ''))
            if release_date:
                movie, created = Movies.objects.update_or_create(
                    api_id=movie_data['id'],
                    defaults={
                        'title': movie_data['title'],
                        'description': movie_data['overview'],
                        'rating': movie_data['vote_average'],
                        'release_date': release_date,
                        'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get('poster_path') else '',
                        'video_url': movie_data.get('video', ''),
                        'movie_categories': 'Movie'
                    }
                )
                genre_ids = movie_data.get('genre_ids', [])
                category_objects = get_or_create_categories(genre_ids)
                movie.categories.set(category_objects)
                movie.save()

        cartoon_data = fetch_cartoon_movies(api_key, 'Panda')
        for data in cartoon_data['results']:
            release_date = parse_date(data.get('release_date', ''))
            if release_date:
                cartoon, created = Movies.objects.update_or_create(
                    api_id=data['id'],
                    defaults={
                        'title': data['title'],
                        'description': data['overview'],
                        'rating': data['vote_average'],
                        'release_date': release_date,
                        'poster_url': f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else '',
                        'movie_categories': 'Cartoon'
                    }
                )
                genre_ids = data.get('genre_ids', [])
                category_objects = get_or_create_categories(genre_ids)
                cartoon.categories.set(category_objects)
                cartoon.save()

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored movies and their categories.'))
