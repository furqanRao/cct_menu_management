from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(RestaurantMenu)
admin.site.register(MenuVote)
admin.site.register(Winner)
