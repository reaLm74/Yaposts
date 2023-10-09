from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Group, Comment, Follow
from users.models import Profile

User = get_user_model()


def get_related_field(many=False, read_only=True):
    return serializers.SlugRelatedField(
        many=many, read_only=read_only, slug_field='id'
    )


class PostSerializer(serializers.ModelSerializer):
    author = get_related_field()
    group = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Group.objects.all(),
        default=None
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'is_published')


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        lookup_field = 'slug'
        fields = ('title', 'description', 'slug', 'posts')


class CommentSerializer(serializers.ModelSerializer):
    author = get_related_field()

    class Meta:
        model = Comment
        fields = ('author', 'text', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'author',)
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
            ),
        )

    def validate(self, data):
        if data['author'] == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data


class FollowListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('author',)


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')


class FavouriteSerializer(serializers.ModelSerializer):
    favourite = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('favourite',)
