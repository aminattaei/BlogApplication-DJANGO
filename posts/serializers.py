from rest_framework import serializers
from .models import Category, Post, Comment, Tag
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        author = serializers.StringRelatedField()
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_time",
            "image",
        ]
