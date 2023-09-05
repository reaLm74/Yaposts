from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ContactForm


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


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
