from django import forms
from tabnanny import verbose
from django.db import models
from django.utils import timezone

category_of_choice = (('diary', '日記'), ('python', 'パイソン'))
tag_of_choice = (('diary', '日記'), ('python', 'パイソン'))

class BlogModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='タイトル')
    body = models.TextField(verbose_name='本文')
    post_datetime = models.DateTimeField(default=timezone.now, verbose_name='投稿日時')
    category = models.CharField(max_length=40, choices=category_of_choice, verbose_name='カテゴリー')
    tag = forms.MultipleChoiceField(choices=tag_of_choice)
    
    def __str__(self):
        return self.title