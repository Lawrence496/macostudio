# Generated by Django 5.0.6 on 2024-06-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='if_watched',
            field=models.BooleanField(default=False),
        ),
    ]
