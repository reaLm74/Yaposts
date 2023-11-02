from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import NewsletterForm
from .models import Newsletters
from .tasks import send_email


class NewsletterView(CreateView):
    model = Newsletters
    form_class = NewsletterForm
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.save()
        send_email.delay(form.instance.email)
        return super().form_valid(form)
