from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Movies(models.Model):
    MOVIE_TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Series', 'TV Series'),
        ('Cartoon', 'Cartoon')
    ]
    
    title = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='movies', default='Action') 
    movie_categories = models.CharField(max_length=255, choices=MOVIE_TYPE_CHOICES, default='Movie')
    description = models.TextField()
    rating = models.DecimalField(decimal_places=1, max_digits=4)
    release_date = models.DateField(blank=True, null=True)
    poster_url = models.URLField()
    video_url = models.URLField(blank=True, null=True)
    screenshot_urls = models.JSONField(default=list, blank=True)
    api_id = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

class VideoWatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        
class Series(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='series', default='Action') 
    poster_url = models.CharField(max_length=400)
    api_id = models.IntegerField(unique=True) 
    first_air_date = models.DateField(blank=True, null=True)
    number_of_seasons = models.IntegerField()
    number_of_episodes = models.IntegerField()
    screenshot_urls = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(decimal_places=1, max_digits=4, blank=True, null=True)

    def __str__(self):
        return self.title

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes', on_delete=models.CASCADE)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    air_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.series.title} S{self.season_number}E{self.episode_number} - {self.title}"
           
class Reviews(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='reviews')
    series = models.ForeignKey(Series, on_delete=models.CASCADE,  related_name='reviews_series', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        
class MovieInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    action = models.CharField(max_length=20) 
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'movie', 'action')
        
class UserGenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username}'s genre preferences"

