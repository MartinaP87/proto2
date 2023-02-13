from django.urls import path
from events import views

urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/<int:pk>', views.EventDetail.as_view()),
    path('events/galleries/', views.GalleryList.as_view()),
    path('events/galleries/<int:pk>', views.GalleryDetail.as_view()),
    path('events/galleries/photos', views.PhotoList.as_view()),
    path('events/galleries/photos/<int:pk>', views.PhotoDetail.as_view()),
]
