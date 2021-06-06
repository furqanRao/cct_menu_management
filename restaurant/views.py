from django.contrib.auth import authenticate, login, logout
from datetime import date, timedelta
import traceback
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, UserCreateSerializer, RestaurantSerializer, RestaurantMenuSerializer, \
    MenuListSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from django.db.models import Count
from django.db.models import Q

import logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(__name__)


class LoginView(APIView):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "username and password are required!"
            })
        user = authenticate(username=username, password=password)
        if user:
            try:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "token": token.key,
                    "message": "Login Successful!"
                }
            except:
                response = {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Due to internal error we couldn't process your request, please try again later!"
                }
        else:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "User not found!"
            }
        return Response(response)


class CreateEmployeeView(CreateAPIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCreateSerializer


class CreateRestaurantView(CreateAPIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    serializer_class = RestaurantSerializer


class CreateRestaurantMenuView(CreateAPIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    serializer_class = RestaurantMenuSerializer


class GetRestaurantsMenuView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = RestaurantMenu.objects.filter(created_at=date.today())
    serializer_class = MenuListSerializer


class MenuVoteView(APIView):

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        menu_id = request.POST.get('menu_id')
        menu = RestaurantMenu.objects.filter(id=menu_id)
        if token:
            token = token.split(' ')[1]
        else:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "token": "Authentication Credentials were not provided!"
            })
        if menu_id and menu:
            token_obj = Token.objects.get(key=token)
            if not MenuVote.objects.filter(employee=token_obj.user, created_at=date.today()):
                MenuVote.objects.create(employee=token_obj.user, menu=menu[0], created_at=date.today())
                return Response({
                    "status": status.HTTP_200_OK,
                    "token": "You have successfully Voted for today's {}'s Menu:{}!".format(menu[0].restaurant.name,
                                                                                            menu[0].menu_item)
                })
            else:
                menu_obj = MenuVote.objects.get(employee=token_obj.user, created_at=date.today())
                return Response({
                    "status": status.HTTP_208_ALREADY_REPORTED,
                    "message": "You've already voted for today's {}'s Menu:{}!".format(menu[0].restaurant.name,
                                                                                       menu_obj.menu.menu_item)
                })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Please make sure you're supplying menu_id and it is correct!"
            })


class GetTodayWinner(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        # today's total votes group by restaurant
        total_votes = (MenuVote.objects.filter(created_at=date.today()).values(
                        'menu_id', 'menu__restaurant_id').annotate(dcount=Count('employee')).order_by('-dcount'))
        if total_votes:
            # last two days consecutive winners
            last_winner = Winner.objects.filter(Q(created_at__lt=date.today()) &
                                                Q(created_at__gte=date.today() - timedelta(days=2)))
            last_winner_ids = [i.menu.restaurant.id for i in last_winner]
            try:
                menu_id = total_votes[0]['menu_id']
                total = total_votes[0]['dcount']
                menu__restaurant_id = total_votes[0]['menu__restaurant_id']

                # checking if the today's winner is last two days consecutive winner also
                if last_winner_ids.count(menu__restaurant_id) == 2:

                    # checking if there's a runner up winner
                    if len(total_votes) > 1:
                        menu_id = total_votes[1]['menu_id']
                        total = total_votes[1]['dcount']
                    else:
                        return Response({
                            "status": status.HTTP_200_OK,
                            "Winner": "Today's Winner was last two days consecutive winner, "
                                      "it cannot be today's winner again!"
                        })
                if Winner.objects.filter(created_at=date.today()):
                    winner = Winner.objects.get(created_at=date.today())
                    winner.menu_id = menu_id
                    winner.votes = int(total)
                    winner.save()
                else:
                    winner = Winner.objects.create(menu_id=menu_id, votes=int(total))
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Today's Winner is {}'s Menu:{} with {} votes!".format(winner.menu.restaurant.name,
                                                                                      winner.menu.menu_item,
                                                                                      total)
                })
            except:
                print(traceback.print_exc())
                return Response({
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Due to internal error we couldn't process your request, please try again later!"
                })
        else:
            return Response({
                "status": status.HTTP_204_NO_CONTENT,
                "message": "No Vote casted Yet!"
            })


class Logout(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            Token.objects.filter(key=token).delete()
        except:
            print(traceback.print_exc())
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Logged Out Successfully!"
        })
