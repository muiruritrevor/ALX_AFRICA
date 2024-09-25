from django.shortcuts import render
from .serializers import Userserializer
from rest_framework import mixins, generics
from django.contrib.auth.models import User

# Mixin - They are reusable optional actions like -> list, retrieve, update, create 


class UserCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializer

    def post (self, request, *args, **kwargs): 
        return self.create(request, *args, **kwargs)
    




# Create your views here.
