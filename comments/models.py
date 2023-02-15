from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment {self.content} by {self.owner.username}"
