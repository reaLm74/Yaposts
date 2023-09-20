from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('about/', include('about.urls', namespace='about')),
    path('posts_load/', include('posts_load.urls', namespace='posts_load')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls', namespace='api')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

handler403 = 'core.views.page_403'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.page_500'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

urlpatterns += doc_url
