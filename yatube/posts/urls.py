from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('group/<slug:slug>/', views.GroupPosts.as_view(), name='group_list'),
    path('post_create/', views.PostCreate.as_view(), name='create_post'),
    path('posts/<int:post_id>/delete_post/', views.PostDelete.as_view(),
         name='delete_post'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('posts/<int:post_id>/', views.PostDetail.as_view(),
         name='post_detail'),
    path('posts/<int:post_id>/edit/', views.PostEdit.as_view(),
         name='post_edit'),
    path('posts/<int:post_id>/comment/', views.AddComment.as_view(),
         name='add_comment'),
    path('posts/follow/', views.FollowIndex.as_view(), name='follow_index'),
    path('posts/<str:username>/follow/', views.AuthorsFollowing.profile_follow,
         name='profile_follow'),
    path('posts/<str:username>/unfollow/',
         views.AuthorsFollowing.profile_unfollow, name='profile_unfollow'),
    path('posts/authors_following/', views.AuthorsFollowing.as_view(),
         name='authors_following'),
    path('posts/posts_favourite/', views.PostsFavourite.as_view(),
         name='posts_favourite'),
    path('posts/<int:post_id>/favourite/', views.PostsFavourite.post_favourite,
         name='post_favourite'),
    path('posts/<int:post_id>/del_favourite/',
         views.PostsFavourite.post_del_favourite, name='post_del_favourite'),
]
