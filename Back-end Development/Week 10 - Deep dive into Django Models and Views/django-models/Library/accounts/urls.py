from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register, profile, logout_view 
# from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'), 
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
