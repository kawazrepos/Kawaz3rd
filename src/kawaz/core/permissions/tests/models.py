from django.db import models

class Article(models.Model):
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'permissions'