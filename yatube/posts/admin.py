import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Group


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', 'is_published', 'get_image', 'day_created_post')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('group', 'is_published')
    list_per_page = 10
    fields = ('text', 'group', ('image', 'get_image'), 'author', 'is_published', 'pub_date',)
    readonly_fields = ('get_image', 'pub_date',)
    actions = ['del_group']

    @admin.display(description="Миниатюра")
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')

    # get_image.short_description = "Миниатюра" - в декораторе

    @admin.display(ordering="-pub_date", description="Дней от создания поста")
    def day_created_post(self, obj):
        create_post = datetime.datetime.today().date() - obj.pub_date.date()
        return create_post.days

    # day_created_post.short_description = "Дней от создания поста"

    @admin.action(description="Удалить группу")
    def del_group(self, request, obj):
        count_updater = obj.update(group=None)
        self.message_user(request, f'Было обновлено {count_updater} записей')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10


# admin.site.register(Post, PostAdmin) - заменен декоратором
# admin.site.register(Group, GroupAdmin)

admin.site.site_title = "Управление статьями"
admin.site.site_header = "Управление статьями"
