# movies/management/commands/fetch_series_data.py

from django.core.management.base import BaseCommand
from movies.models import Movies, Series, Episode
import requests

class Command(BaseCommand):
    help = 'Fetch TV Series data from TMDb and save it to the database'

    def handle(self, *args, **kwargs):
        api_key = '2af8f53d7614f389368f9ee77ab3d464'  # Replace with your actual TMDb API key
        tv_series = Movies.objects.filter(movie_categories__iexact='TV Series')

        for movie in tv_series:
            try:
                url = f'https://api.themoviedb.org/3/tv/{movie.api_id}?api_key={api_key}'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    series, created = Series.objects.update_or_create(
                        api_id=movie.api_id,
                        defaults={
                            'title': data['name'],
                            'description': data['overview'],
                            'poster_url': data['poster_path'],
                            'first_air_date': data.get('first_air_date', None),
                            'number_of_seasons': data['number_of_seasons'],
                            'number_of_episodes': data['number_of_episodes'],
                        }
                    )

                    for season in data['seasons']:
                        season_number = season['season_number']
                        season_url = f'https://api.themoviedb.org/3/tv/{movie.api_id}/season/{season_number}?api_key={api_key}'
                        season_response = requests.get(season_url)
                        if season_response.status_code == 200:
                            season_data = season_response.json()
                            for episode in season_data['episodes']:
                                Episode.objects.update_or_create(
                                    series=series,
                                    season_number=season_number,
                                    episode_number=episode['episode_number'],
                                    defaults={
                                        'title': episode['name'],
                                        'air_date': episode.get('air_date', None),
                                        'description': episode['overview'],
                                    }
                                )
                    self.stdout.write(self.style.SUCCESS(f"Successfully saved data for {data['name']}"))
                else:
                    self.stderr.write(self.style.ERROR(f"Failed to fetch data for {movie.title}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing {movie.title}: {e}"))
