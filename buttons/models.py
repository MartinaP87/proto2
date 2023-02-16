from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from comments.models import Comment


class Interested(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'posted_event']

    def __str__(self):
        return f"{self.owner} {self.posted_event}"


class Going(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'posted_event']

    def __str__(self):
        return f"{self.owner} {self.posted_event}"


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'comment']

    def __str__(self):
        return f"{self.owner} {self.comment}"
