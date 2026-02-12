import graphene
from graphene_django.types import ErrorType
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import Post
from .decorators import login_required_graphql
from .types import PostType, UserType
from .serializers import PostSerializer


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    errors = graphene.List(ErrorType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        # author_id = graphene.String(required=True)

    @login_required_graphql
    def mutate(parent, info, title, description=None):
        author_id = info.context.user.id
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

    @login_required_graphql
    def mutate(parent, info, id, title=None, description=None):
        queryset = Post.objects.filter(author_id=info.context.user.id)
        post = get_object_or_404(queryset, pk=id)
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

    @login_required_graphql
    def mutate(parent, info, id):
        try:
            post = Post.objects.filter(id=id, author_id=info.context.user.id).first()
            if post:
                post.delete()
                return DeletePost(success=True, errors=[])
            errors = [ErrorType(field="errors", messages=["Post Not Found!"])]
            return DeletePost(success=False, errors=errors)
        except Exception as e:
            errors = [ErrorType(field="errors", messages=[str(e)])]
            return DeletePost(success=False, errors=errors)


class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    error = graphene.Field(ErrorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(parent, info, username, password):
        request = info.context  # info.context is the request in graphene django
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request=request, user=user)
            return Login(user=user, success=True, error=None)
        error = ErrorType(field="error", messages=["Invalid Creadentials."])
        return Login(user=None, success=False, error=error)


class Logout(graphene.Mutation):
    success = graphene.Boolean()
    error = graphene.Field(ErrorType)

    class Arguments:
        pass

    @login_required_graphql
    def mutate(parent, info):
        request = info.context
        logout(request=request)
        return Logout(success=True, error=None)
