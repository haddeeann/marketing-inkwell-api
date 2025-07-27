from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


User = get_user_model()


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published",
            "created_at",
            "author",
            "tags"
        ]
        read_only_fields = ['id', 'author', 'slug']

    def get_author(self, obj):
        """
        Return a human-readable name:
        1. `full_name` if you added that field,
        2. else `obj.author.get_full_name()` (first + last),
        3. else fallback to `username`.
        """
        user = obj.author
        return (
                getattr(user, "full_name", None)
                or user.get_full_name()
                or user.username
        )
