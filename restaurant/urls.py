from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('create_employee', views.CreateEmployeeView.as_view(), name='create_employee'),
    path('create_restaurant', views.CreateRestaurantView.as_view(), name='create_restaurant'),
    path('create_menu', views.CreateRestaurantMenuView.as_view(), name='create_menu'),
    path('get_menu', views.GetRestaurantsMenuView.as_view(), name='get_menu'),
    path('vote_menu', views.MenuVoteView.as_view(), name='vote_menu'),
    path('get_winner', views.GetTodayWinner.as_view(), name='get_winner')
]
