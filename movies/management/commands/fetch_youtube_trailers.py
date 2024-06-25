from googleapiclient.discovery import build
from django.core.management.base import BaseCommand
from movies.models import Movies

class Command(BaseCommand):
    help = 'Fetch and update YouTube trailers for movies in the database'

    def handle(self, *args, **kwargs):
        youtube_api_key = '**************************'
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
        # Fetching all movies from the database
        movies = Movies.objects.all()

        for movie in movies:
            query = f"{movie.title} trailer"
            
            # Calling the YouTube API to search for the trailer
            request = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=1,
                videoEmbeddable='true', 
                videoSyndicated='true'  
            )
            
            response = request.execute()
            
            # Checking if any trailers were found
            if response['items']:
                video = response['items'][0]
                video_id = video['id']['videoId']
                video_url = f"https://www.youtube-nocookie.com/embed/{video_id}"
                
                # Updating the movie's video_url field with embedded video URL
                movie.video_url = video_url
                movie.save()
                
                self.stdout.write(self.style.SUCCESS(f"Updated {movie.title} with embedded trailer URL: {video_url}"))
            else:
                self.stdout.write(self.style.WARNING(f"No trailer found for {movie.title}"))

