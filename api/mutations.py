import graphene
from graphene_django.types import ErrorType
from django.shortcuts import get_object_or_404
from .models import Post
from .types import PostType
from .serializers import PostSerializer


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    errors = graphene.List(ErrorType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        author_id = graphene.String(required=True)

    def mutate(parent, info, title, author_id, description=None):
        serializer = PostSerializer(
            data={"title": title, "author": author_id, "description": description}
        )
        if serializer.is_valid():
            post = serializer.save()
            return CreatePost(post=post, errors=[])

        errors = [
            ErrorType(field=field, messages=messages)
            for field, messages in serializer.errors.items()
        ]
        return CreatePost(post=None, errors=errors)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    errors = graphene.List(ErrorType)

    class Arguments:
        id = graphene.String(required=True)
        title = graphene.String()
        description = graphene.String()

    def mutate(parent, info, id, title=None, description=None):
        post = get_object_or_404(Post, pk=id)
        data = dict()
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        serializer = PostSerializer(
            instance=post,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            post = serializer.save()
            return UpdatePost(post=post, errors=[])

        errors = [
            ErrorType(field=field, messages=messages)
            for field, messages in serializer.errors.items()
        ]
        return UpdatePost(post=None, errors=errors)


class DeletePost(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        id = graphene.String(required=True)

    def mutate(parent, info, id):
        try:
            post = Post.objects.filter(id=id).first()
            if post:
                post.delete()
                return DeletePost(success=True, errors=[])
            errors = [ErrorType(field="errors", messages=["Post Not Found!"])]
            return DeletePost(success=False, errors=errors)
        except Exception as e:
            errors = [ErrorType(field="errors", messages=[str(e)])]
            return DeletePost(success=False, errors=errors)
