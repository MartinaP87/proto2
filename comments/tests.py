from django.contrib.auth.models import User
from .models import Comment
from events.models import Event
from categories.models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')

    def test_can_list_comments(self):
        marla = User.objects.get(username='marla')
        event = Event.objects.get(pk=1)
        Comment.objects.create(
            owner=marla, posted_event=event, content='nice!')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_comment(self):
        event = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/comments/', {'posted_event': event.id,
                           'content': 'nice!'})
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_a_comment(self):
        event = Event.objects.get(pk=1)
        response = self.client.post(
            '/comments/', {'posted_event': event.id,
                           'content': 'nice!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        event = Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')
        comment1 = Comment.objects.create(
            owner=marla, posted_event=event, content='nice!')
        comment2 = Comment.objects.create(
            owner=peter, posted_event=event, content='wow!')

    def test_can_retrieve_a_comment_using_valid_id(self):
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['content'], 'nice!')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_a_comment_using_invalid_id(self):
        response = self.client.get('/comments/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        event = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/comments/1/', {'posted_event': event.id,
                             'content': 'very nice!'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'very nice!')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_comment(self):
        event = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/comments/2/', {'posted_event': event.id,
                             'content': 'very nice!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comment(self):
        comment1 = Comment.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/comments/1/')
        response2 = self.client.get('comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_comment(self):
        comment2 = Comment.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/comments/2/')
        response2 = self.client.get('/comments/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
