from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import serializers
from .permissions import IsAuthorOrReadOnly
from posts.models import Comment, Group, Post, User, Follow


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (
        permissions.AllowAny,
    )


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments.all()

    def get_object(self):
        object = get_object_or_404(Comment, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, object)
        return object

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_id']
        )


class FollowViewSet(generics.ListCreateAPIView):
    serializer_class = serializers.FollowSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('following',)
    search_fields = ('following__username', 'following__id')

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        user = self.request.user
        following = get_object_or_404(
            User,
            username=self.request.data['following']
        )
        if following == user:
            raise ValidationError('Подписка на самого себя невозможна')
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError('Такая подписка уже существует')
        return serializer.save(
            user=self.request.user
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer = serializers.UserSerializer
