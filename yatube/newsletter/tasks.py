from datetime import datetime, timedelta

from posts.models import Post
from yatube.celery import app
from .models import Newsletters
from .service import send, send_to_newsletter


@app.task
def send_email(user_email):
    send(user_email)


@app.task
def send_new_posts():
    stage = datetime.now() - timedelta(minutes=60 * 24 * 7)
    posts = Post.objects.filter(pub_date__gte=stage)
    contacts = Newsletters.objects.all()
    if len(posts) != 0:
        send_to_newsletter(contacts, posts)
