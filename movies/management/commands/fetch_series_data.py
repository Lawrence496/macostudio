from django.core.management.base import BaseCommand
from movies.models import Series, Episode, Category
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches and stores TV series and their episodes from the TMDb API'

    def handle(self, *args, **kwargs):
        api_key = '************************'

        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None
        
        genres_url = f'https://api.themoviedb.org/3/genre/tv/list?api_key={api_key}&language=en-US'
        genres_response = requests.get(genres_url)
        if genres_response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Error fetching genres: {genres_response.status_code} - {genres_response.text}"))
            return
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

        def fetch_series(api_key, query):
            series_url = f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}'
            response = requests.get(series_url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Error fetching series: {response.status_code} - {response.text}"))
                return {}
            return response.json()

        def fetch_series_details(api_key, series_id):
            details_url = f'https://api.themoviedb.org/3/tv/{series_id}?api_key={api_key}&language=en-US'
            response = requests.get(details_url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Error fetching series details for ID {series_id}: {response.status_code} - {response.text}"))
                return {}
            return response.json()

        series_data = fetch_series(api_key, 'Power')
        if 'results' not in series_data:
            self.stdout.write(self.style.ERROR(f"'results' key not found in series_data: {series_data}"))
            return

        for series in series_data['results']:
            detailed_series_data = fetch_series_details(api_key, series['id'])
            if not detailed_series_data:
                continue

            first_air_date = parse_date(series.get('first_air_date', ''))
            screenshot_urls = [f"https://image.tmdb.org/t/p/w500{series['backdrop_path']}"] if series.get('backdrop_path') else []

            tv_series, created = Series.objects.update_or_create(
                api_id=series['id'],
                defaults={
                    'title': series['name'],
                    'description': series['overview'],
                    'rating': series['vote_average'],
                    'first_air_date': first_air_date,
                    'poster_url': f"https://image.tmdb.org/t/p/w500{series['poster_path']}" if series.get('poster_path') else '',
                    'number_of_seasons': detailed_series_data.get('number_of_seasons', 0),
                    'number_of_episodes': detailed_series_data.get('number_of_episodes', 0),
                    'screenshot_urls': screenshot_urls,
                }
            )
            genre_ids = series.get('genre_ids', [])
            category_objects = get_or_create_categories(genre_ids)
            tv_series.categories.set(category_objects)
            tv_series.save()

            for season_number in range(1, detailed_series_data.get('number_of_seasons', 0) + 1):
                season_url = f'https://api.themoviedb.org/3/tv/{series["id"]}/season/{season_number}?api_key={api_key}&language=en-US'
                season_response = requests.get(season_url)
                if season_response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"Error fetching season {season_number}: {season_response.status_code} - {season_response.text}"))
                    continue
                season_data = season_response.json()
                for episode in season_data.get('episodes', []):
                    air_date = parse_date(episode.get('air_date', ''))
                    Episode.objects.update_or_create(
                        series=tv_series,
                        season_number=season_number,
                        episode_number=episode['episode_number'],
                        defaults={
                            'title': episode['name'],
                            'air_date': air_date,
                            'description': episode['overview']
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored series and episodes.'))
