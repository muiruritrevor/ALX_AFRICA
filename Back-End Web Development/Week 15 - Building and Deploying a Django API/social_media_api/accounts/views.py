from django.shortcuts import redirect
from rest_framework import permissions, generics
from .serializers import CustomUserSerializer
from .models import CustomUser


class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permissions_class = [permissions.AllowAny]


    def get(self, request):
        return redirect('login')
    
class Loginview()


# Create your views here.
