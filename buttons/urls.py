from django.urls import path
from buttons import views

urlpatterns = [
    path('interested/', views.InterestedList.as_view()),
    path('interested/<int:pk>/', views.InterestedDetail.as_view()),
    path('going/', views.GoingList.as_view()),
    path('going/<int:pk>/', views.GoingDetail.as_view()),
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view())
    ]
