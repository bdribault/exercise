import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Profile

JOHN_DIC = {
    "id": 1,
    "username": "John Doe",
    "birthday": "12/09/1976",
}

JOHN_DETAILED_DIC = {
    "id": 1,
    "username": "John Doe",
    "birthday": "12/09/1976",
    "is_superuser": False,
    "is_staff": False,
}


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.john = User.objects.create_user(username='John Doe')
        self.john_profile = Profile.objects.create(user=self.john, birthday=datetime.date(1976, 9, 12))

        maggy_birthday = datetime.datetime.now() - datetime.timedelta(days=3 * 365 + 20)
        self.maggy = User.objects.create_user(username='Maggy Doe')
        self.maggy_profile = Profile.objects.create(user=self.maggy, birthday=maggy_birthday)

    def test_age(self):
        # John was born on 1976, he will always be more than 40 years
        self.assertGreaterEqual(self.john_profile.age, 40)

        # Maggy's birthday is relative, she will always be 3 year old
        self.assertEqual(self.maggy_profile.age, 3)

    def test_get_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

        user_list = response.json()
        self.assertEqual(len(user_list), 2)

        self.assertDictEqual(user_list[0], JOHN_DIC)

    def test_get_details(self):
        response = self.client.get('/users/1')

        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(response.json(), JOHN_DETAILED_DIC)

    def test_year_filter(self):
        # Nobody born on 1900
        self.assertEqual(self.client.get('/users/?year=1900').json(), [])

        # Only John born on 1976
        result_list = self.client.get('/users/?year=1976').json()
        self.assertEqual(len(result_list), 1)
        self.assertDictEqual(result_list[0], JOHN_DIC)

    def test_age_filter(self):
        # Nobody is 20 year old
        self.assertEqual(self.client.get('/users/?age=20').json(), [])

        # Maggy is 3 year old
        self.assertEqual(self.client.get('/users/?age=3').json()[0]["username"], "Maggy Doe")

    def test_min_max_filters(self):
        # Maggy's 3 age is between 1 and 5
        self.assertEqual(self.client.get('/users/?min_age=1&max_age=5').json()[0]["username"], "Maggy Doe")

