from django.urls import path
from .views import NewsletterView

app_name = 'newsletter'

urlpatterns = [
    path('', NewsletterView.as_view(), name='newsletter')
]
