from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import CreationForm
from django.contrib.auth import login


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # Автоматическая авторизация при регистрации
        user = form.save()
        login(self.request, user)
        return redirect('posts:index')
