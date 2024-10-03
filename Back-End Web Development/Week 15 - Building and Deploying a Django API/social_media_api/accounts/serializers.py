from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','username', 'email', 'password', 'bio')

    def create(self, validated_data):
        CustomUser = CustomUser.objects.create_user(**validated_data)
        return CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 

    def validate(self, data):
        user = CustomUser.objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError('User not found')
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Incorrect password')
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        