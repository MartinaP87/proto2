from django.contrib import admin
from .models import Event, Gallery, Photo, EventGenre

admin.site.register(Event)
admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(EventGenre)
