from django.urls import include, path

from .views import cat_list, post_list

app_name = 'api'

urlpatterns = [
   path('cats/', cat_list),
   path('post/', post_list),
]