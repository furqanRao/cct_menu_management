# Generated by Django 3.2.3 on 2021-06-03 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_winner_restaurant_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winner',
            name='restaurant_id',
        ),
    ]
