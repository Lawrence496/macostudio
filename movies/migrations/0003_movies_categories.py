# Generated by Django 5.0.6 on 2024-06-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='categories',
            field=models.ManyToManyField(related_name='movies', to='movies.category'),
        ),
    ]
