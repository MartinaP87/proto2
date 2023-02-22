from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from categories.models import Category, Genre


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/', blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['title', 'date', 'location']

    def __str__(self):
        return self.title


class Gallery(models.Model):
    name = models.CharField(max_length=250, default="Gallery")
    posted_event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.posted_event} {self.name}"


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.title}"


class EventGenre(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_genres')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.genre.gen_name


def create_gallery(sender, instance, created, **kwargs):
    if created:
        Gallery.objects.create(posted_event=instance)


post_save.connect(create_gallery, sender=Event)
