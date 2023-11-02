from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Еженедельная рассылка свежих новостей.',
        'gew@mail.com',
        [user_email],
        fail_silently=False,
    )


def send_to_newsletter(contact, posts):
    """Рассылка писем пользователям на их подписки"""
    subject, from_email, to = 'Новое на Yaposts', 'from@example.com', contact
    text_content = f'Уведомление о новых постах'
    html_content = render_to_string(
        'newsletter/newsletter_email.html', {'posts': posts}
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
