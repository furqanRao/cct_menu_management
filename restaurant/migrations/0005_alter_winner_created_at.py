# Generated by Django 3.2.3 on 2021-06-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='created_at',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
    ]
