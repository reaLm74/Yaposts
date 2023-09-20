from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Group, Follow
from users.models import Profile
from .permissions import AuthorOrReadOnly
from .serializers import (PostSerializer, UserSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer,
                          FollowListSerializer, FavouriteSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)

    # Вывод через action
    # @action(detail=True)
    # def group(self, request, pk=None):
    #     group = get_object_or_404(Group, slug=self.kwargs['pk'])
    #     schedule = Post.objects.filter(group=group).distinct()
    #     schedule_json = PostSerializer(schedule, many=True)
    #     return Response(schedule_json.data)
    #
    # @action(detail=True)
    # def author(self, request, pk=None):
    #     author = get_object_or_404(User, username=self.kwargs['pk'])
    #     schedule = Post.objects.filter(author=author).distinct()
    #     schedule_json = PostSerializer(schedule, many=True)
    #     return Response(schedule_json.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Post.objects.filter(author__following__user=user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'slug'
    permission_classes = (AuthorOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AuthorOrReadOnly,)


class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=kwargs['pk'])
        obj = Follow.objects.filter(user=self.request.user, author=author)
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'list':
            return FollowListSerializer
        return FollowSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        return get_object_or_404(User, username=self.request.user)

    def get_queryset(self):
        user = Profile.objects.filter(user=self.get_user())
        return user

    def perform_create(self, serializer):
        user = self.get_user()
        post = serializer.data['favourite'][0]
        post = get_object_or_404(Post, pk=post)
        favourite = user.profile.favourite.filter(pk=post).exists()
        if user != post.author and not favourite:
            user.profile.favourite.add(post)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_user()
        post = get_object_or_404(Post, pk=kwargs['pk'])
        favourite = request.user.profile.favourite.filter(
            pk=kwargs['pk']
        ).exists()
        if not favourite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.profile.favourite.remove(post)
        return Response(status=status.HTTP_204_NO_CONTENT)
