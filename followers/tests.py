from django.contrib.auth.models import User
from .models import Follower
from rest_framework import status
from rest_framework.test import APITestCase


class FollowerListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')
        User.objects.create_user(username='peter', password='pass')

    def test_can_list_followers(self):
        marla = User.objects.get(username='marla')
        peter = User.objects.get(username='peter')
        Follower.objects.create(owner=marla, followed=peter)
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_follower(self):
        peter = User.objects.get(username='peter')
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/followers/', {'followed': peter.id})
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_follower(self):
        peter = User.objects.get(username='peter')
        response = self.client.post(
            '/followers/', {'followed': peter.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FollowerDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        follower1 = Follower.objects.create(owner=marla, followed=peter)
        follower2 = Follower.objects.create(owner=peter, followed=marla)

    def test_can_retrieve_follower_using_valid_id(self):
        response = self.client.get('/followers/1/')
        self.assertEqual(response.data['owner'], 'marla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_follower_using_invalid_id(self):
        response = self.client.get('/followers/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_follower(self):
        follower1 = Follower.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/followers/1/')
        response2 = self.client.get('followers/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_follower(self):
        follower2 = Follower.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/followers/2/')
        response2 = self.client.get('/followers/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
