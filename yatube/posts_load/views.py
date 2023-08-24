from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from posts.models import Post

from .forms import PostLoadForm


class PostLoad(LoginRequiredMixin, FormView):
    template_name = 'posts_load/posts_load.html'
    model = Post
    form_class = PostLoadForm
    login_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        posts_file = form.cleaned_data['file'].read()
        posts_str = posts_file.decode('utf-8').split('/r')
        author = self.request.user
        for text in posts_str:
            Post.objects.create(text=text, author=author)
        return super().form_valid(form)  # Можно сделать страницу со статусом об успешном наполнении

    def get_success_url(self):
        return reverse_lazy('posts:index')
