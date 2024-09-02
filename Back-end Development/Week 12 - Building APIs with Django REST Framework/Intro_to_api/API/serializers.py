"""Serializers simplify the process of converting complex data structures such as Django Models 
into formats like JSON and XML"""

from rest_framework import serializers
from .models import Book, Author

"""BookSerializer handles both serialization and deserialization of instances of book model """
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # specifies which model fields should be inclusded in the serialized output 

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, data):
        if len(data['name']) < 5:
            raise serializers.ValidationError("Name must be at least 5 characters long.")

        return data