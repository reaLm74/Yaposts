from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import *

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'follow', FollowViewSet, basename='follow')
router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comment')
router_v1.register(r'follower', FollowerViewSet, basename='follower')
router_v1.register(r'user', UserViewSet, basename='user')
router_v1.register(r'posts_favourite', FavouriteViewSet, basename='favourite')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]
