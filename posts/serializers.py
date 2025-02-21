from rest_framework import serializers
from .models import Category, Post, Comment, Tag, Contact
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        # author = serializers.StringRelatedField()
        author = UserSerializer(read_only=True, many=True)
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
    comments = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "message", "created_time"]
