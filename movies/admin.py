from django.contrib import admin
from .models import Movies, Category, Reviews, VideoWatch, MovieInteraction, UserGenrePreference, Series, Episode
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'movie_categories', 'release_date', 'video_url')
    
    search_fields = ('title', 'movie_categories')
    sortable_by = ['rating']
    list_filter = ('rating', 'release_date', 'movie_categories')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'number_of_seasons')
    
admin.site.register(Movies, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reviews)
admin.site.register(VideoWatch)
admin.site.register(MovieInteraction)
admin.site.register(UserGenrePreference)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Episode)