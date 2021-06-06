from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, RestaurantMenu, MenuVote
from datetime import date


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', ]


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["email"] = validated_data["username"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name')

    def create(self, validated_data):
        name = validated_data.pop('name')
        owner = User.objects.filter(is_superuser=True)[0]
        restaurant, created = Restaurant.objects.get_or_create(user=owner, name=name)
        return restaurant


class RestaurantMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMenu
        fields = '__all__'

    def create(self, validated_data):
        if not RestaurantMenu.objects.filter(restaurant=validated_data['restaurant'], created_at=date.today()):
            return RestaurantMenu.objects.create(**validated_data)
        else:
            raise serializers.ValidationError({
                'Error': "Sorry, You can not have more than one Menu for a Restaurant per day!"
            })


class MenuListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = RestaurantMenu
        fields = ('restaurant', 'id', 'menu_item', 'detail', 'created_at')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuVote
        fields = '__all__'

    def create(self, validated_data):
        if not MenuVote.objects.filter(employee=validated_data['restaurant'], created_at=date.today()):
            return MenuVote.objects.create(**validated_data)
        else:
            raise serializers.ValidationError({
                'Error': "Sorry, You can only vote once for a Menu per day!"
            })
