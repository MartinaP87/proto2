from django.contrib.auth.models import User
from .models import Profile, Interest
from categories.models import Category, Genre
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')

    def test_can_list_profiles(self):
        marla = User.objects.get(username='marla')
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_creates_when_a_user_is_created(self):
        marla = User.objects.get(username='marla')
        response = self.client.get('/profiles/1/')
        count = Profile.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')

    def test_can_retrieve_profile_using_valid_id(self):
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.data['owner'], 'marla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_profile_using_invalid_id(self):
        response = self.client.get('/profiles/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profile(self):
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/profiles/1/', {'owner': 'marla',
                             'name': 'marla'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.name, 'marla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_profile(self):
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/profiles/2/', {'owner': 'peter',
                             'name': 'marla'})
        profile = Profile.objects.filter(pk=2).first()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InterestListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')
        category = Category.objects.create(cat_name='music')
        genre1 = Genre.objects.create(category=category, gen_name='Rock')
        genre2 = Genre.objects.create(category=category, gen_name='Folk')

    def test_can_list_preferences(self):
        marla = User.objects.get(username='marla')
        profile = Profile.objects.get(owner=marla)
        genre = Genre.objects.get(pk=1)
        Interest.objects.create(profile=profile, genre=genre)
        response = self.client.get('/profiles/interests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_preference(self):
        genre = Genre.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/profiles/interests/', {'genre': genre.id})
        count = Interest.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_preference(self):
        genre = Genre.objects.get(pk=2)
        response = self.client.post(
            '/profiles/interests/', {'genre': genre.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PreferenceDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')
        User.objects.create_user(username='peter', password='pass')
        marla = Profile.objects.get(pk=1)
        peter = Profile.objects.get(pk=2)
        category = Category.objects.create(cat_name='music')
        genre1 = Genre.objects.create(category=category, gen_name='Rock')
        genre2 = Genre.objects.create(category=category, gen_name='Folk')
        interest1 = Interest.objects.create(profile=marla, genre=genre1)
        interest2 = Interest.objects.create(profile=peter, genre=genre2)

    def test_can_retrieve_preference_using_valid_id(self):
        genre1 = Genre.objects.get(pk=1)
        response = self.client.get('/profiles/interests/1/')
        self.assertEqual(response.data['genre'], genre1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_preference_using_invalid_id(self):
        response = self.client.get('/profiles/interests/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_preference(self):
        genre2 = Genre.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/profiles/interests/1/', {'genre': genre2.id})
        preference = Interest.objects.filter(pk=1).first()
        self.assertEqual(preference.genre, genre2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_preference(self):
        genre1 = Genre.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/profiles/interests/2/', {'genre': genre1.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_preference(self):
        preference1 = Interest.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/profiles/interests/1/')
        response2 = self.client.get('/profiles/interests/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_preference(self):
        preference2 = Interest.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/profiles/interests/2/')
        response2 = self.client.get('/profiles/interests/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
