from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ContactForm


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Здесь можно произвести какие-то действия для создания контекста.
    #     # Для примера в словарь просто передаются две строки
    #     context['just_title'] = 'Очень простая страница'
    #     context['just_text'] = ('На создание этой страницы '
    #                             'у меня ушло пять минут! Ай да я.')
    #     return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'


class ContactView(FormView):
    template_name = 'about/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        send_mail(
            form.cleaned_data['name'],
            form.cleaned_data['text'],
            form.cleaned_data['email'],
            ['geoche74@gmail.com'],
            fail_silently=False,
        )
        return super().form_valid(form)
