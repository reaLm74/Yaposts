from django.db import models


class Newsletters(models.Model):
    email = models.EmailField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
