from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from .validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    title = models.TextField(verbose_name='Имя')
    slug = models.SlugField(max_length=15, verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ('pk',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # В админке создает ссылку на просмотр и можно использовать
        # как удобную ссылку в шаблоне как метод функции
        return reverse('posts:group_list', kwargs={'slug': self.slug})


class Post(models.Model):
    # text = models.TextField(
    #     verbose_name='Текст',
    #     validators=[validate_not_empty]
    # ) # убран для текстового редактора
    text = RichTextUploadingField(
        verbose_name='Текст',
        validators=[validate_not_empty]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Сообщество',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Публикация',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.text[:15]

    def get_absolute_url(self):
        # В админке создает ссылку на просмотр и можно использовать
        # как удобную ссылку в шаблоне как метод функции
        return reverse('posts:post_detail', kwargs={'post_id': self.pk})

    def get_delete_url(self):
        return reverse('posts:delete_post', kwargs={'post_id': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Кто подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписываются'
    )


@receiver(post_save, sender=Post)
def send_to_sub(sender, **kwargs):
    """Рассылка писем пользователям на их подписки"""
    followers = Follow.objects.filter(user=kwargs['instance'].author).values_list('author__email')
    subject, from_email, to = 'Subject here', 'from@example.com', followers
    text_content = f'Уведомление о новой статье автора: {kwargs["instance"].author.get_full_name()}'
    html_content = render_to_string('posts/email.html', {'Title': 'Тестовое'})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    pass
