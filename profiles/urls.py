from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>', views.ProfileDetail.as_view()),
    path('profiles/interests/', views.InterestList.as_view()),
    path('profiles/interests/<int:pk>', views.InterestDetail.as_view()),
]
