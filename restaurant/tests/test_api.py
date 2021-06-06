from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Restaurant, RestaurantMenu, MenuVote
from rest_framework.test import APITestCase


class AuthenticationTestCase(APITestCase):

    def setUp(self):
        self.data = {
            "username": "employee",
            "password": "very-strong-pass"
        }
        self.new_user_data = {
            "username": "new_employee",
            "password": "very-strong-pass"
        }
        self.wrong_data = {
            "username": "employee",
            "password": "weak-pass"
        }
        # create superuser
        self.user = User.objects.create_superuser(username="admin", password="very-strong-pass")
        self.token = Token.objects.create(user=self.user)
        # create employee
        self.employee = User.objects.create_user(username="employee", password="very-strong-pass")
        self.employee_token = Token.objects.create(user=self.employee)

    # in case of creating same user again
    def test_create_same_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/restaurant/create_employee", self.data)
        self.assertEqual(response.status_code, 400)

    # in case of success
    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/restaurant/create_employee", self.new_user_data)
        self.assertEqual(response.status_code, 201)

    # in case of invalid token
    def test_do_not_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key+"extra")
        response = self.client.post("/restaurant/create_employee", self.data)
        # print("not create: ", response.data)
        self.assertEqual(response.status_code, 401)

    # in case of successful login
    def test_login_view(self):
        response = self.client.post("/restaurant/login", self.data)
        self.assertEqual(response.data['status'], 200)

    # in case of login fail because credentials are incorrect
    def test_can_not_login_view(self):
        response = self.client.post("/restaurant/login", self.wrong_data)
        self.assertEqual(response.data['status'], 404)

    # in case of valid logout
    def test_logout_view(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token.key)
        response = self.client.post("/restaurant/logout", self.data)
        self.assertEqual(response.data['status'], 200)

    # in case of invalid logout
    def test_can_not_logout_view(self):
        response = self.client.post("/restaurant/logout", self.data)
        self.assertEqual(response.status_code, 401)


class RestaurantTestCase(APITestCase):

    def setUp(self):
        # create Admin and token
        self.user = User.objects.create_superuser(username="admin", password="very-strong-pass")
        self.token = Token.objects.create(user=self.user)

        # create employee/user and token
        self.employee = User.objects.create_user(username="employee", password="very-strong-pass")
        self.employee_token = Token.objects.create(user=self.employee)

        self.employee2 = User.objects.create_user(username="employee2", password="very-strong-pass")
        self.employee_token2 = Token.objects.create(user=self.employee2)

        self.employee3 = User.objects.create_user(username="employee3", password="very-strong-pass")
        self.employee_token3 = Token.objects.create(user=self.employee3)

        self.employee4 = User.objects.create_user(username="employee4", password="very-strong-pass")
        self.employee_token4 = Token.objects.create(user=self.employee4)

        self.employee5 = User.objects.create_user(username="employee5", password="very-strong-pass")
        self.employee_token5 = Token.objects.create(user=self.employee5)

        # create Restaurant for creating the menu
        self.restaurant = Restaurant.objects.create(user=self.user, name="New Pizza Hut")
        self.restaurant2 = Restaurant.objects.create(user=self.user, name="New Domino's")
        self.restaurant3 = Restaurant.objects.create(user=self.user, name="New Papa Johns")
        self.restaurant4 = Restaurant.objects.create(user=self.user, name="New California Pizza")
        self.restaurant5 = Restaurant.objects.create(user=self.user, name="New Brazilian")

        # create today's menu for voting
        self.menu1 = RestaurantMenu.objects.create(restaurant=self.restaurant, menu_item="Chicken",
                                                   detail="We have Chicken Today")
        self.menu2 = RestaurantMenu.objects.create(restaurant=self.restaurant2, menu_item="Rice",
                                                   detail="We have Rice Today")
        self.menu3 = RestaurantMenu.objects.create(restaurant=self.restaurant3, menu_item="Trifle",
                                                   detail="We have Trifle Today")

        # employees vote
        self.vote1 = MenuVote.objects.create(menu=self.menu1, employee=self.employee)
        self.vote2 = MenuVote.objects.create(menu=self.menu1, employee=self.employee2)
        self.vote3 = MenuVote.objects.create(menu=self.menu2, employee=self.employee3)
        self.vote4 = MenuVote.objects.create(menu=self.menu1, employee=self.employee4)

        self.user_data = {
            "username": "test_username",
            "password": "strong-Pas$w0rd"
        }
        self.restaurant_data = {
            "name": "new_restaurant",
        }
        self.menu_data = {
            "restaurant": 5,
            "menu_item": "new_menu_item",
            "detail": "We have Chicken in Lunch",
        }
        self.vote_data = {
            "menu_id": RestaurantMenu.objects.all()[0].id,
        }

    # in case of error (Employee can not create restaurant)
    def test_fail_creating_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token.key)
        response = self.client.post("/restaurant/create_restaurant", self.restaurant_data)
        self.assertEqual(response.status_code, 403)

    # in case of success (Only Admin can create restaurants)
    def test_create_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/restaurant/create_restaurant", self.restaurant_data)
        self.assertEqual(response.status_code, 201)

    # in case of error (Employee can not create menu)
    def test_fail_creating_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token.key)
        response = self.client.post("/restaurant/create_menu", self.menu_data)
        self.assertEqual(response.status_code, 403)

    # in case of success (Only Admin can create menu)
    def test_create_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/restaurant/create_menu", self.menu_data)
        self.assertEqual(response.status_code, 201)

    # in case of error(getting without passing the authentication token)
    def test_fail_get_today_menu(self):
        response = self.client.get("/restaurant/get_menu")
        self.assertEqual(response.status_code, 401)

    # in case of success
    def test_get_today_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token.key)
        response = self.client.get("/restaurant/get_menu")
        self.assertEqual(response.status_code, 200)

    # in case of error(getting without passing the authentication token)
    def test_fail_vote_menu(self):
        response = self.client.post("/restaurant/vote_menu", self.vote_data)
        self.assertEqual(response.data['status'], 401)

    # in case of success
    def test_vote_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token5.key)
        response = self.client.post("/restaurant/vote_menu", self.vote_data)
        self.assertEqual(response.data['status'], 200)

    # in case of error(getting without passing the authentication token)
    def test_fail_get_winner(self):
        response = self.client.get("/restaurant/get_winner")
        self.assertEqual(response.status_code, 401)

    # in case of success
    def test_get_winner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.employee_token5.key)
        response = self.client.get("/restaurant/get_winner")
        print("\nWinner: ", response.data['message'])
        self.assertEqual(response.status_code, 200)
