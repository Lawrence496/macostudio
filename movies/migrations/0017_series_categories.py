# Generated by Django 5.0.6 on 2024-06-23 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_series_rating_series_screenshot_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='categories',
            field=models.ManyToManyField(default='Action', related_name='series', to='movies.category'),
        ),
    ]
