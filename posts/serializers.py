from rest_framework import serializers
from .models import Category, Post, Comment, Tag,Contact
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=[
            'name',
            'email',
            'message',
            'created_at'
        ]
        
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=[
            'name',
            'message',
            'created_time'
        ]