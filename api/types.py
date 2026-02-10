from graphene_django import DjangoObjectType

import graphene
from django.contrib.auth.models import User
from .models import Post, Comment


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "posts",
            "comments",
            "date_joined",
        )


class PostType(DjangoObjectType):
    word_count = graphene.Int()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "author",
            "comments",
            "created_at",
            "modified_at",
        )

    def resolve_word_count(self, info):
        return len(self.description.split()) if self.description else 0


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "content", "user", "post", "created_at", "modified_at")
