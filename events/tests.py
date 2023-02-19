from django.contrib.auth.models import User
from .models import Event, Category
from rest_framework import status
from rest_framework.test import APITestCase


class EventListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')
        Category.objects.create(cat_name='concert')

    def test_can_list_events(self):
        concert = Category.objects.get(cat_name='concert')
        marla = User.objects.get(username='marla')
        Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30', location='a location', address='an address')
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(len(response.data))

    def _logged_in_user_can_create_an_event(self):
        concert = Category.objects.get(cat_name='concert')
        self.client.login(username='marla', password='pass')
        response = self.client.post('/events/', {'title': 'a title',
                                                 'category': concert,
                                                 'date': '2020-11-28T19:24:58.478641+05:30',
                                                 'location': 'a location',
                                                 'address': 'an address'})
        count = Event.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_event(self):
        concert = Category.objects.get(cat_name='concert')
        response = self.client.post('/events/', {'title': 'a title',
                                                 'category': concert,
                                                 'date': '2020-11-28T19:24:58.478641+05:30',
                                                 'location': 'a location',
                                                 'address': 'an address'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventDetailViewTests(APITestCase):
    def setUp(self):
        Category.objects.create(cat_name='concert')
        concert = Category.objects.get(cat_name='concert')
        marla = User.objects.create_user(username='marla', password='pass')
        adam = User.objects.create_user(username='adam', password='pass')
        Event.objects.create(owner=marla, title='a title', category=concert,
                             date='2020-11-28T19:24:58.478641+05:30',
                             location='a location',
                             address='an address')
        Event.objects.create(owner=adam, title='another title',
                             category=concert,
                             date='2020-11-28T19:24:58.478641+05:30',
                             location='another location',
                             address='another address')

    def test_can_retrieve_event_using_valid_id(self):
        response = self.client.get('/events/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_event_using_invalid_id(self):
        response = self.client.get('/events/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_event(self):
        concert = Category.objects.get(cat_name='concert')
        self.client.login(username='marla', password='pass')
        response = self.client.put('/events/1/', {'title': 'a new title',
                                                  'category': concert,
                                                  'date': '2020-11-28T19:24:58.478641+05:30',
                                                  'location': 'a location',
                                                  'address': 'an address'})
        event = Event.objects.filter(pk=1).first()
        self.assertEqual(event.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_event(self):
        concert = Category.objects.get(cat_name='concert')
        self.client.login(username='marla', password='pass')
        response = self.client.put('/events/2/', {'title': 'a new title',
                                                  'category': concert,
                                                  'date': '2020-11-28T19:24:58.478641+05:30',
                                                  'location': 'a location',
                                                  'address': 'an address'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
