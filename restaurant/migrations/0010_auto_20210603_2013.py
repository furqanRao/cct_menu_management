# Generated by Django 3.2.3 on 2021-06-03 20:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_remove_winner_restaurant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuvote',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='restaurantmenu',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
