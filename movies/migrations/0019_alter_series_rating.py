# Generated by Django 5.0.6 on 2024-06-23 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_alter_series_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
    ]
