# management/commands/update_series_data.py

from django.core.management.base import BaseCommand
from movies.models import Series, Category
import requests

class Command(BaseCommand):
    help = 'Updating ratings and genres for Series from TMDb'

    def handle(self, *args, **kwargs):
        api_key = '2af8f53d7614f389368f9ee77ab3d464'
        series = Series.objects.all()

        for series_obj in series:
            try:
                url = f'https://api.themoviedb.org/3/tv/{series_obj.api_id}?api_key={api_key}'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    rating = data.get('vote_average', None)
                    if rating:
                        series_obj.rating = rating

                    genres = data.get('genres', [])
                    if genres:
                        series_obj.categories.clear() 
                        for genre in genres:
                            genre_name = genre.get('name')
                            category_obj, created = Category.objects.get_or_create(category=genre_name)
                            series_obj.categories.add(category_obj)

                    series_obj.save()

                    self.stdout.write(self.style.SUCCESS(f"Updated data for {series_obj.title}"))
                else:
                    self.stderr.write(self.style.ERROR(f"Failed to fetch data for {series_obj.title}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing {series_obj.title}: {e}"))
