from django.contrib.auth.models import User
from .models import Category, Genre
from rest_framework import status
from rest_framework.test import APITestCase


class CategoryListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_superuser(
            username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')

    def test_can_list_categories(self):
        marla = User.objects.get(username='marla')
        Category.objects.create(
            cat_name='music')
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuse_user_can_create_a_category(self):
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/categories/', {'cat_name': 'music'})
        count = Category.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cant_add_a_category(self):
        self.client.login(username='peter', password='pass')
        response = self.client.post(
            '/categories/', {'cat_name': 'art'})
        response2 = self.client.get('/categories/1/')
        count = Category.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_not_logged_in_cant_create_a_category(self):
        response = self.client.post(
            '/categories/', {'cat_name': 'music'})
        count = Category.objects.count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_superuser(
            username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        categoy1 = Category.objects.create(cat_name='music')
        categoy2 = Category.objects.create(cat_name='art')

    def test_can_retrieve_a_category_using_valid_id(self):
        response = self.client.get('/categories/1/')
        self.assertEqual(response.data['cat_name'], 'music')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_a_category_using_invalid_id(self):
        response = self.client.get('/categories/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_update_category(self):
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/categories/1/', {'cat_name': 'cinema'})
        category = Category.objects.filter(pk=1).first()
        self.assertEqual(category.cat_name, 'cinema')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_category(self):
        self.client.login(username='peter', password='pass')
        response = self.client.put(
            '/categories/1/', {'cat_name': 'cinema'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_category(self):
        category1 = Category.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/categories/1/')
        response2 = self.client.get('/categories/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_category(self):
        category1 = Category.objects.get(pk=1)
        self.client.login(username='peter', password='pass')
        response = self.client.delete('/categories/1/')
        response2 = self.client.get('/categories/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class GenreListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_superuser(
            username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        category = Category.objects.create(cat_name='music')

    def test_can_list_genres(self):
        marla = User.objects.get(username='marla')
        category = Category.objects.get(pk=1)
        Genre.objects.create(category=category, gen_name='Rock')
        response = self.client.get('/categories/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuse_user_can_create_a_genre(self):
        music = Category.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/categories/genres/', {'category': music.id,
                                    'gen_name': 'Prog'})
        count = Genre.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cant_add_a_genre(self):
        music = Category.objects.get(pk=1)
        self.client.login(username='peter', password='pass')
        response = self.client.post(
            '/categories/genres/', {'cat_name': music.id})
        response2 = self.client.get('/categories/genres/1/')
        count = Genre.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_not_logged_in_cant_create_a_genre(self):
        music = Category.objects.get(pk=1)
        response = self.client.post(
            '/categories/genres/', {'cat_name': music.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GenreDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_superuser(
            username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        category = Category.objects.create(cat_name='music')
        genre = Genre.objects.create(category=category, gen_name='Prog')

    def test_can_retrieve_a_genre_using_valid_id(self):
        response = self.client.get('/categories/genres/1/')
        self.assertEqual(response.data['gen_name'], 'Prog')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_a_genre_using_invalid_id(self):
        response = self.client.get('/categories/genres/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_update_genre(self):
        category = Category.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/categories/genres/1/', {'category': category.id,
                                      'gen_name': 'Metal'})
        genre = Genre.objects.filter(pk=1).first()
        self.assertEqual(genre.gen_name, 'Metal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_genre(self):
        category = Category.objects.get(pk=1)
        self.client.login(username='peter', password='pass')
        response = self.client.put(
            '/categories/genres/1/', {'category': category.id,
                                      'gen_name': 'Metal'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_genre(self):
        genre = Genre.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/categories/genres/1/')
        response2 = self.client.get('/categories/genres/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_category(self):
        genre = Genre.objects.get(pk=1)
        self.client.login(username='peter', password='pass')
        response = self.client.delete('/categories/genres/1/')
        response2 = self.client.get('/categories/genres/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
