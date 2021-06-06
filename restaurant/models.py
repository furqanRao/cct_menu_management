from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, default="Restaurant", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_item = models.CharField(max_length=255, default="Simple Menu")
    detail = models.TextField(default="Simple Menu Detail")
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.restaurant.name + "-" + self.menu_item


class MenuVote(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.employee.username + " -> " + self.menu.menu_item + " -> " + str(self.menu.created_at)


class Winner(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.menu.menu_item + "-" + str(self.created_at)
