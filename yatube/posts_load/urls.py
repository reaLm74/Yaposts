from django.urls import path
from . import views

app_name = 'posts_load'

urlpatterns = [
    path('', views.PostLoad.as_view(), name='posts_load'),
]
