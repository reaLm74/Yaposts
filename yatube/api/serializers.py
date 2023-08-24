from rest_framework import serializers

from .models import Cat
from posts.models import Post


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ('name', 'color', 'birth_year')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'pub_date', 'author', 'group')
