from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.PostIndex.as_view(), name='index'),
    # path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('group/<slug:slug>/', views.GroupPosts.as_view(), name='group_list'),
    path('post_create/', views.PostCreate.as_view(), name='create_post'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    # path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/edit/', views.PostEdit.as_view(), name='post_edit'),
    # path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comment/', views.AddComment.as_view(), name='add_comment'),
    # path('posts/follow/', views.follow_index, name='follow_index'),
    path('posts/follow/', views.FollowIndex.as_view(), name='follow_index'),
    path('posts/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    # path('posts/<str:username>/follow/', views.ProfileFollow.as_view(), name='profile_follow'),
    path('posts/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    # path('posts/authors_following/', views.authors_following, name='authors_following'),
    path('posts/authors_following/', views.AuthorsFollowing.as_view(), name='authors_following'),
]
