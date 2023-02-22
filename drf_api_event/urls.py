from django.contrib import admin
from django.urls import path, include
from .views import root_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include(
        'dj_rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('profiles.urls')),
    path('', include('categories.urls')),
    path('', include('events.urls')),
    path('', include('buttons.urls')),
    path('', include('comments.urls')),
    path('', include('followers.urls')),
]
