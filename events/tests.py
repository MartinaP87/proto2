from django.contrib.auth.models import User
from .models import Event, Gallery, Photo, EventGenre
from categories.models import Category, Genre
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image
import io


class EventListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='marla', password='pass')
        Category.objects.create(cat_name='concert')

    def test_can_list_events(self):
        concert = Category.objects.get(cat_name='concert')
        marla = User.objects.get(username='marla')
        Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_an_event(self):
        Category.objects.get(cat_name='concert')
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/events/', {'title': 'a title',
                         'category': '1',
                         'date': '2020-11-28T19:24:58.478641+05:30',
                         'location': 'a location',
                         'address': 'an address'})
        count = Event.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_event(self):
        concert = Category.objects.get(cat_name='concert')
        response = self.client.post(
            '/events/', {'title': 'a title',
                         'category': concert,
                         'date': '2020-11-28T19:24:58.478641+05:30',
                         'location': 'a location',
                         'address': 'an address'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventDetailViewTests(APITestCase):
    def setUp(self):
        concert = Category.objects.create(cat_name='concert')
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
        response = self.client.put(
            '/events/1/', {'title': 'a new title',
                           'category': '1',
                           'date': '2020-11-28T19:24:58.478641+05:30',
                           'location': 'a location',
                           'address': 'an address'})
        event = Event.objects.filter(pk=1).first()
        self.assertEqual(event.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_event(self):
        concert = Category.objects.get(cat_name='concert')
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/events/2/', {'title': 'a new title',
                           'category': '1',
                           'date': '2020-11-28T19:24:58.478641+05:30',
                           'location': 'a location',
                           'address': 'an address'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_event(self):
        event = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/1/')
        response2 = self.client.get('/events/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_event(self):
        event = Event.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/2/')
        response2 = self.client.get('/events/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class GalleryListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        concert = Category.objects.create(cat_name='concert')
        event = Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='a location',  address='an address')

    def test_can_list_galleries(self):
        response = self.client.get('/events/galleries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_galley_creates_when_an_event_is_created(self):
        concert = Category.objects.get(cat_name='concert')
        marla = User.objects.get(username='marla')
        event2 = Event.objects.create(
            owner=marla, title='second title', category=concert,
            date='2020-11-22T19:24:58.478641+05:30',
            location='second location',  address='second address')

        response = self.client.get('/events/galleries/2/')
        count = Gallery.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GalleryDetailViewTests(APITestCase):
    def setUp(self):
        concert = Category.objects.create(cat_name='concert')
        marla = User.objects.create_user(username='marla', password='pass')
        adam = User.objects.create_user(username='adam', password='pass')
        Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='a location',
            address='an address')
        Event.objects.create(
            owner=adam, title='another title',
            category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='another location',
            address='another address')
        gallery1 = Gallery.objects.get(pk=1)
        gallery2 = Gallery.objects.get(pk=2)

    def test_can_retrieve_gallery_using_valid_id(self):
        event1 = Event.objects.get(pk=1)
        response = self.client.get('/events/galleries/1/')
        self.assertEqual(response.data['posted_event'], event1.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_gallery_using_invalid_id(self):
        response = self.client.get('/events/galleries/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_event_gallery(self):
        event1 = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/events/galleries/1/', {'name': 'a new name',
                                     'posted_event': event1.title})
        gallery = Gallery.objects.filter(pk=1).first()
        self.assertEqual(gallery.name, 'a new name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_event_category(self):
        event2 = Event.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.put(
            '/events/galleries/2/', {'name': 'a different name',
                                     'posted_event': event2.title})
        gallery = Gallery.objects.filter(pk=2).first()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PhotoListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        concert = Category.objects.create(cat_name='concert')
        event = Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='a location',  address='an address')

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_can_list_photos(self):
        gallery = Gallery.objects.get(pk=1)
        peter = User.objects.get(username='peter')
        Photo.objects.create(
            owner=peter, title='a photo', gallery=gallery)
        photo = Photo.objects.get(pk=1)
        response = self.client.get('/events/galleries/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_photo(self):
        gallery = Gallery.objects.get(pk=1)
        self.client.login(username='peter', password='pass')
        photo_file = self.generate_photo_file()
        response = self.client.post('/events/galleries/photos/',
                                    {'title': 'a photo',
                                     'image': photo_file,
                                     'gallery': 1})
        count = Photo.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_photo(self):
        gallery = Gallery.objects.get(pk=1)
        photo_file = self.generate_photo_file()
        response = self.client.post('/events/galleries/photos/',
                                    {'title': 'a new photo',
                                     'image': photo_file,
                                     'gallery': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PhotoDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        concert = Category.objects.create(cat_name='concert')
        event1 = Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='a location',  address='an address')
        event2 = Event.objects.create(
            owner=peter, title='another title',
            category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='another location',
            address='another address')
        gallery1 = Gallery.objects.get(pk=1)
        gallery2 = Gallery.objects.get(pk=2)
        photo1 = Photo.objects.create(owner=marla, title='a photo',
                                      gallery=gallery1)
        photo2 = Photo.objects.create(owner=peter, title='a photo',
                                      gallery=gallery2)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_can_retrieve_photo_using_valid_id(self):
        response = self.client.get('/events/galleries/photos/1/')
        self.assertEqual(response.data['title'], 'a photo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_photo_using_invalid_id(self):
        response = self.client.get('/events/galleries/photos/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_photo(self):
        self.client.login(username='marla', password='pass')
        photo_file = self.generate_photo_file()
        response = self.client.put(
            '/events/galleries/photos/1/', {'title': 'a new photo title',
                                            'image': photo_file,
                                            'gallery': 1})
        photo = Photo.objects.filter(pk=1).first()
        self.assertEqual(photo.title, 'a new photo title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_photo(self):
        self.client.login(username='marla', password='pass')
        photo_file = self.generate_photo_file()
        response = self.client.put(
            '/events/galleries/photos/2/', {'title': 'a new photo title',
                                            'image': photo_file,
                                            'gallery': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_photo(self):
        photo = Photo.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/galleries/photos/1/')
        response2 = self.client.get('/events/galleries/photos/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_photo(self):
        photo = Photo.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/galleries/photos/2/')
        response2 = self.client.get('/events/galleries/photos/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class EventGenreListViewTests(APITestCase):
    def setUp(self):
        concert = Category.objects.create(cat_name='concert')
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        Event.objects.create(owner=marla, title='a title', category=concert,
                             date='2020-11-28T19:24:58.478641+05:30',
                             location='a location',
                             address='an address')
        Event.objects.create(owner=peter, title='another title',
                             category=concert,
                             date='2020-11-28T19:24:58.478641+05:30',
                             location='another location',
                             address='another address')

    def test_can_list_event_genres(self):
        category = Category.objects.create(cat_name='concert')
        genre = Genre.objects.create(category=category, gen_name='Rock')
        event = Event.objects.get(pk=1)
        EventGenre.objects.create(event=event, genre=genre)
        response = self.client.get('/events/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_owner_can_create_an_eventgenre(self):
        self.client.login(username='marla', password='pass')
        event = Event.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        genre = Genre.objects.create(category=category, gen_name='Rock')
        response = self.client.post(
            '/events/genres/', {'genre': genre.id,
                                'event': event.id})
        count = EventGenre.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_event_owner_cant_create_eventgenre(self):
        self.client.login(username='marla', password='pass')
        event = Event.objects.get(pk=2)
        category = Category.objects.get(pk=1)
        genre = Genre.objects.create(category=category, gen_name='Rock')
        response = self.client.post(
            '/events/genres/', {'genre': genre.id,
                                'event': event.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_cant_create_eventgenre_if_category_doesnt_match_the_events(
            self):
        self.client.login(username='marla', password='pass')
        event = Event.objects.get(pk=1)
        category = Category.objects.create(cat_name='movie night')
        genre = Genre.objects.create(category=category, gen_name='Horror')
        response = self.client.post(
            '/events/genres/', {'genre': genre.id,
                                'event': event.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventGenreDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        concert = Category.objects.create(cat_name='concert')
        genre1 = Genre.objects.create(category=concert, gen_name='Metal')
        genre2 = Genre.objects.create(category=concert, gen_name='Folk')
        event1 = Event.objects.create(
            owner=marla, title='a title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='a location', address='an address')
        event2 = Event.objects.create(
            owner=peter, title='another title', category=concert,
            date='2020-11-28T19:24:58.478641+05:30',
            location='another location', address='another address')
        eventgenre1 = EventGenre.objects.create(event=event1, genre=genre1)
        eventgenre2 = EventGenre.objects.create(event=event2, genre=genre2)

    def test_can_retrieve_eventgenre_using_valid_id(self):
        genre1 = Genre.objects.get(pk=1)
        response = self.client.get('/events/genres/1/')
        self.assertEqual(response.data['genre'], genre1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_gallery_using_invalid_id(self):
        response = self.client.get('/events/genres/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_eventgenre(self):
        self.client.login(username='marla', password='pass')
        event1 = Event.objects.get(pk=1)
        genre2 = Genre.objects.get(pk=2)
        eventgenre1 = EventGenre.objects.get(pk=1)
        response = self.client.put(
            '/events/genres/1/', {'event': event1.id,
                                  'genre': genre2.id})
        eventgenre1 = EventGenre.objects.filter(pk=1).first()
        self.assertEqual(eventgenre1.genre, genre2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_cant_update_eventgenre_if_category_doesnt_match_the_events(
            self):
        self.client.login(username='marla', password='pass')
        event = Event.objects.get(pk=1)
        category = Category.objects.create(cat_name='movie night')
        genre = Genre.objects.create(category=category, gen_name='Horror')
        response = self.client.put(
            '/events/genres/1/', {'genre': genre.id,
                                  'event': event.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_update_another_users_event_category(self):
        self.client.login(username='peter', password='pass')
        event1 = Event.objects.get(pk=1)
        genre2 = Genre.objects.get(pk=2)
        eventgenre1 = EventGenre.objects.get(pk=1)
        response = self.client.put(
            '/events/genres/1/', {'event': event1.id,
                                  'genre': genre2.id})
        eventgenre1 = EventGenre.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_eventgenre(self):
        eventgenre1 = EventGenre.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/genres/1/')
        response2 = self.client.get('/events/genres/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_eventgenre(self):
        eventgenre2 = EventGenre.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/events/genres/2/')
        response2 = self.client.get('/events/genres/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
