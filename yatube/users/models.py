from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Post


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    tel = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name='Телефон',
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Адрес',
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    favourite = models.ManyToManyField(
        Post,
    )

    class Meta:
        verbose_name = 'Телефон, адрес, дата рождения'
        verbose_name_plural = 'Телефоны, адреса, даты рождений'
        ordering = ('user',)

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
