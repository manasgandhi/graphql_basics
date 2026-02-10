import graphene
from django.shortcuts import get_object_or_404
from .models import Post, User, Comment
from .types import UserType, PostType, CommentType
from .utils import get_requested_fields
from .mutations import CreatePost, UpdatePost, DeletePost


class Query(graphene.ObjectType):
    post = graphene.Field(PostType, id=graphene.String(required=True))
    all_posts = graphene.List(
        PostType,
        author_id=graphene.String(),
        title_contains=graphene.String(),
        created_after=graphene.DateTime(),
        created_before=graphene.DateTime(),
    )
    user = graphene.Field(UserType, id=graphene.String(required=True))
    all_users = graphene.List(
        UserType,
        user_id=graphene.String(),
        username_contains=graphene.String(),
        created_after=graphene.DateTime(),
        created_before=graphene.DateTime(),
    )
    user_posts = graphene.List(PostType, author_id=graphene.String(required=True))
    comment = graphene.Field(CommentType, id=graphene.String(required=True))

    def resolve_post(root, info, id):
        return get_object_or_404(Post, pk=id)

    def resolve_all_posts(
        root,
        info,
        author_id=None,
        title_contains=None,
        created_after=None,
        created_before=None,
    ):
        fields = get_requested_fields(info=info)

        queryset = Post.objects.all()
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if title_contains:
            queryset = queryset.filter(title__icontains=title_contains)
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        if created_before:
            queryset = queryset.filter(created_at__lte=created_before)
        if "author" in fields:
            queryset = queryset.select_related("author")
        if "comments" in fields:
            queryset = queryset.prefetch_related("comments")

        return queryset

    def resolve_user(root, info, id):
        return get_object_or_404(User, pk=id)

    def resolve_all_users(
        root,
        info,
        user_id=None,
        username_contains=None,
        created_after=None,
        created_before=None,
    ):
        fields = get_requested_fields(info=info)
        queryset = User.objects.all()
        if user_id:
            queryset = queryset.filter(id=user_id)
        if username_contains:
            queryset = queryset.filter(username__icontains=username_contains)
        if created_after:
            queryset = queryset.filter(date_joined__gte=created_after)
        if created_before:
            queryset = queryset.filter(date_joined__lte=created_before)

        if "posts" in fields:
            queryset = queryset.prefetch_related("posts")
        if "comments" in fields:
            queryset = queryset.prefetch_related("comments")
        return queryset

    def resolve_user_posts(root, info, author_id):
        fields = get_requested_fields(info=info)
        queryset = Post.objects.filter(author_id=author_id).all()
        if "author" in fields:
            queryset = queryset.select_related("author")
        if "comments" in fields:
            queryset = queryset.prefetch_related("comments")
        return queryset

    def resolve_comment(root, info, id):
        return get_object_or_404(Comment, pk=id)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
