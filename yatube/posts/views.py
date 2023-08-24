from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .forms import PostForm, CommentForm
from .models import Post, Follow, Comment

User = get_user_model()


# def index(request):
#     title = "Последние обновления на сайте"
#     post_list = Post.objects.filter(is_published=True)
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'title': title,
#         'posts': page_obj,
#     }
#     return render(request, 'posts/index.html', context)

class PostIndex(ListView):
    # Аналог def index(request): через ListView
    paginate_by = 10
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    extra_context = {'title': "Последние обновления на сайте"}

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author')

    # def get_context_data(self, *, object_list=None, **kwargs):
    # Применяется когда изменяемые данные (например список)
    # нужно передать в шаблок
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Последние обновления на сайте"
    #     return context


# def group_posts(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     title = f"Записи сообщества {group.title}"
#     post_list = Post.objects.filter(group=group, is_published=True)
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'title': title,
#         'posts': page_obj,
#         'group': group,
#
#     }
#     return render(request, 'posts/group_list.html', context)

class GroupPosts(ListView):
    # Аналог def group_posts(request, slug): через ListView
    paginate_by = 10
    model = Post
    template_name = 'posts/group_list.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Записи сообщества {context['posts'][0].group}"
        return context

    def get_queryset(self):
        return Post.objects.filter(group__slug=self.kwargs['slug'], is_published=True)


# def profile(request, username):
#     author = get_object_or_404(User, username=username)
#     post_list = Post.objects.filter(author=author, is_published=True)
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     amount = len(post_list)
#     following = False
#     if request.user.is_authenticated:
#         following = Follow.objects.filter(
#             user=request.user, author=author
#         ).exists()
#     context = {
#         'posts': page_obj,
#         'author': author,
#         'amount': amount,
#         'following': following
#     }
#     return render(request, 'posts/profile.html', context)


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
        return Post.objects.filter(author__username=self.kwargs['username'])


# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     user = post.author
#     amount = len(Post.objects.filter(author=post.author, is_published=True))
#     author = request.user
#
#     form = CommentForm()
#     comment = post.comments.all()
#     context = {
#         'post': post,
#         'amount': amount,
#         'user': user,
#         'author': author,
#         'form': form,
#         'comments': comment
#     }
#     return render(request, 'posts/post_detail.html', context)


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    pk_url_kwarg = 'post_id'  # имя id поста в urls

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['post_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        context['user'] = self.request.user
        context['author'] = post.author
        context['amount'] = post.author.posts.all().count()
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.kwargs['post_id'])
        return context


# @login_required
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('posts:profile', username=request.user)
#         return render(request, 'posts/create_post.html', {'form': form})
#     form = PostForm()
#     return render(request, 'posts/create_post.html', {"form": form})


class PostCreate(LoginRequiredMixin, CreateView):
    # Аналог def post_create
    template_name = 'posts/create_post.html'
    model = Post
    form_class = PostForm
    login_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:profile', kwargs={'username': self.request.user})


# @login_required
# def post_edit(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.user != post.author:
#         return redirect('posts:post_detail', post_id)
#     form = PostForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=post
#     )
#     if form.is_valid():
#         form.save()
#         return redirect('posts:post_detail', post_id)
#     context = {
#         'form': form,
#         'is_edit': True,
#         'post': post,
#     }
#     return render(request, 'posts/create_post.html', context)

class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'posts/create_post.html'
    model = Post
    fields = ['text', 'group', 'image', 'is_published']
    pk_url_kwarg = 'post_id'
    extra_context = {'is_edit': True}


# @login_required
# def add_comment(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.post = post
#         comment.save()
#     return redirect('posts:post_detail', post_id)


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


# @login_required
# def follow_index(request):
#     post = Post.objects.filter(author__following__user=request.user, is_published=True)
#     paginator = Paginator(post, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     title = f"Подписки"
#     context = {
#         'title': title,
#         'posts': page_obj
#     }
#     return render(request, 'posts/follow.html', context)


class FollowIndex(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Post
    template_name = 'posts/follow.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Подписки"
        return context

    def get_queryset(self):
        return Post.objects.filter(author__following__user=self.request.user, is_published=True)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        following = Follow.objects.filter(author=author, user=request.user).exists()
        if not following:
            Follow.objects.create(user=request.user, author=author)
    return redirect('posts:follow_index')


# class ProfileFollow(LoginRequiredMixin, CreateView):
#     template_name = 'posts/profile.html'
#     model = Follow
#     fields = ['user', 'author',]
#
#     def form_valid(self, form):
#         print(self.request.username)
#         author = get_object_or_404(User, username=self.request.username)
#         form.instance.author = self.request.user
#         return super().form_valid(form)

# class ProfileFollow(LoginRequiredMixin, CreateView):
#     model = Follow
#     template_name = 'posts/create_post.html'
#     fields = []  # Add any additional fields here
#
#     def form_valid(self, form):
#         print('fdfd')
#         author = get_object_or_404(User, username=self.kwargs['username'])
#         if self.request.user != author:
#             following = Follow.objects.filter(author=author, user=self.request.user).exists()
#             if not following:
#                 form.instance.user = self.request.user
#                 form.instance.author = author
#                 Follow.objects.create(user=form.instance.user, author=form.instance.author)
#                 return super().form_valid(form)
#         return redirect('posts:index')
#
#     def get_success_url(self):
#         return reverse_lazy('posts:follow_index')
#


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(author=author, user=request.user).exists()
    if following:
        Follow.objects.filter(
            user=request.user, author=author
        ).delete()
    return redirect('posts:follow_index')


# def authors_following(request):
#     users = Follow.objects.filter(user=request.user)
#     title = "Подписки на авторов"
#     context = {
#         'users': users,
#         'title': title,
#     }
#     return render(request, 'posts/authors_following.html', context)


class AuthorsFollowing(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'posts/authors_following.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = Follow.objects.filter(user=self.request.user)
        context['title'] = "Подписки на авторов"
        context['users'] = users
        return context
