from django.core.management.base import BaseCommand
from movies.models import Movies, Series
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetches screenshots for all movies in the database from TMDb'

    def handle(self, *args, **kwargs):
        api_key = '2af8f53d7614f389368f9ee77ab3d464'
        
        # Iterate over all movies in the database
        movies = Series.objects.all()

        for movie in movies:
            # TMDb search URL to find movie by title
            search_url = f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={movie.title}'
            search_response = requests.get(search_url)
            search_results = search_response.json().get('results', [])

            if search_results:
                # Assume the first search result is the correct one
                tmdb_movie_id = search_results[0]['id']

                # Fetch screenshots (backdrops) for the movie
                screenshots_url = f'https://api.themoviedb.org/3/tv/{tmdb_movie_id}/images?api_key={api_key}'
                screenshots_response = requests.get(screenshots_url)
                screenshots_data = screenshots_response.json().get('backdrops', [])
                
                if screenshots_data:
                    # Construct the full URL for each screenshot
                    screenshot_urls = [f"https://image.tmdb.org/t/p/w500{image['file_path']}" for image in screenshots_data]
                    
                    # Update the movie record with the fetched screenshot URLs
                    movie.screenshot_urls = screenshot_urls
                    movie.save()

                    self.stdout.write(self.style.SUCCESS(f"Updated screenshots for {movie.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No screenshots found for {movie.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"No movie found in TMDb for {movie.title}"))

        self.stdout.write(self.style.SUCCESS('Finished fetching screenshots for all movies.'))
