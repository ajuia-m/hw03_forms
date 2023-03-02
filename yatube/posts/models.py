from django.contrib.auth import get_user_model
from django.db import models

LEN_TEXT = 15

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=32, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор')
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',)

    def __str__(self):
        str_text = ''
        if len(self.text) > 15:
            while len(str_text) <= LEN_TEXT:
                for char in self.text:
                    str_text += char
        else:
            for char in self.text:
                str_text += char
        return str_text
