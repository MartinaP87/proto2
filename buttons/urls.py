from django.urls import path
from buttons import views

urlpatterns = [
    path('interested/', views.InterestedList.as_view()),
    path('interested/<int:pk>/', views.InterestedDetail.as_view()),
    path('going/', views.InterestedList.as_view()),
    path('going/<int:pk>/', views.InterestedDetail.as_view())
    ]
