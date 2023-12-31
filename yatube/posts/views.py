import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView, DetailView, UpdateView,
                                  DeleteView)

from .forms import PostForm, CommentForm
from .models import Post, Follow, Comment, Group

logger = logging.getLogger(__name__)

User = get_user_model()


class PostIndex(ListView):
    paginate_by = 10
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    extra_context = {'title': "Последние обновления на сайте"}

    def get(self, request, *args, **kwargs):
        if search := request.GET.get('search'):
            self.object_list = self.get_queryset(search=search)
        return super().get(self, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if isinstance(self.request.GET.get('search'), str):
            return Post.objects.filter(
                Q(author__first_name__iregex=self.request.GET.get('search')) |
                Q(author__last_name__iregex=self.request.GET.get('search')) |
                Q(text__iregex=self.request.GET.get('search')),
                is_published=True
            ).select_related('author', 'group')
        else:
            return Post.objects.filter(
                is_published=True
            ).select_related('author', 'group')


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    pk_url_kwarg = 'post_id'  # имя id поста в urls

    def get_queryset(self):
        return Post.objects.filter(
            pk=self.kwargs['post_id'],
            is_published=True
        ).select_related('author', 'group').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.all().select_related(
                'author'
            )))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.select_related('author').get(
            pk=self.kwargs['post_id']
        )
        button = False
        favourite = False
        if self.request.user == post.author:
            button = True
        if self.request.user.is_authenticated:
            favourite = self.request.user.profile.favourite.filter(
                pk=post.id
            ).exists()
        context['button'] = button
        context['favourite'] = favourite
        context['amount'] = post.author.posts.all().count()
        context['form'] = CommentForm()
        return context


class GroupPosts(ListView):
    paginate_by = 10
    model = Post
    template_name = 'posts/group_list.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        context['group'] = group
        context['title'] = f"Записи сообщества {group}"
        return context

    def get_queryset(self):
        return Post.objects.filter(
            group__slug=self.kwargs['slug'], is_published=True
        ).select_related('author', 'group')


class Profile(ListView):
    paginate_by = 10
    model = Post
    template_name = 'posts/profile.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'username'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        amount = Post.objects.filter(author=author).count()
        button = True
        following = False
        if self.request.user == author:
            button = False
        if self.request.user.is_authenticated:
            following = Follow.objects.filter(
                user=self.request.user, author=author
            ).exists()
        context['button'] = button
        context['following'] = following
        context['author'] = author
        context['amount'] = amount
        return context

    def get_queryset(self):
        return Post.objects.filter(
            author__username=self.kwargs['username']
        ).select_related('author', 'group')


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_post.html'
    model = Post
    form_class = PostForm
    login_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'posts:profile', kwargs={'username': self.request.user}
        )


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'posts/create_post.html'
    model = Post
    fields = ['text', 'group', 'image', 'is_published']
    pk_url_kwarg = 'post_id'
    extra_context = {'is_edit': True}

    def form_valid(self, form):
        if form.instance.author == self.request.user:
            return super().form_valid(form)
        logger.warning(
            f'Попытка изменения пользователем "{self.request.user}" '
            f'чужого поста: id - {form.instance.pk}'
        )
        return redirect('posts:index')


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'posts/delete_post.html'
    model = Post
    success_url = reverse_lazy('posts:index')
    pk_url_kwarg = 'post_id'


class AddComment(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_detail.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'posts:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class FollowIndex(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Post
    template_name = 'posts/follow.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подписки на авторов'
        return context

    def get_queryset(self):
        return Post.objects.filter(
            author__following__user=self.request.user, is_published=True
        ).select_related('author', 'group')


class AuthorsFollowing(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'posts/authors_following.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = Follow.objects.filter(user=self.request.user).select_related(
            'author')
        context['title'] = "Подписки на авторов"
        context['users'] = users
        return context

    @login_required
    def profile_follow(self, username):
        author = get_object_or_404(User, username=username)
        if self.user != author:
            following = Follow.objects.filter(
                author=author, user=self.user
            ).exists()
            if not following:
                Follow.objects.create(user=self.user, author=author)
        return redirect('posts:follow_index')

    @login_required
    def profile_unfollow(self, username):
        author = get_object_or_404(User, username=username)
        following = Follow.objects.filter(
            author=author, user=self.user
        ).exists()
        if following:
            Follow.objects.filter(
                user=self.user, author=author
            ).delete()
        return redirect('posts:follow_index')


class PostsFavourite(LoginRequiredMixin, ListView):
    model = User
    template_name = 'posts/posts_favourite.html'
    context_object_name = 'posts'

    @staticmethod
    def get_content(self, post_id):
        user = get_object_or_404(User, username=self.user)
        post = get_object_or_404(Post, pk=post_id)
        favourite = user.profile.favourite.filter(pk=post_id).exists()
        return user, post, favourite

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.request.user.profile.favourite.all().select_related(
            'author', 'group'
        )
        context['title'] = "Избранные посты"
        context['posts'] = posts
        return context

    @login_required
    def post_favourite(self, post_id):
        user, post, favourite = PostsFavourite.get_content(self, post_id)
        if user != post.author and not favourite:
            user.profile.favourite.add(post)
            user.save()
        return redirect('posts:post_detail', post_id)

    @login_required
    def post_del_favourite(self, post_id):
        user, post, favourite = PostsFavourite.get_content(self, post_id)
        if favourite:
            user.profile.favourite.remove(post)
            user.save()
        return redirect('posts:post_detail', post_id)
