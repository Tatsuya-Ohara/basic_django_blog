from colorsys import rgb_to_yiq
from django import forms
from tabnanny import verbose
from django.db import models
from django.utils import timezone

# # choiceとしてしまうとソースコード変更しなければ選択肢を変更できない。
# category_of_choice = (('diary', '日記'), ('python', 'パイソン'))
# tag_of_choice = (('diary', '日記'), ('python', 'パイソン'))

class Category(models.Model):
    name= models.CharField(max_length=50, verbose_name='カテゴリ名')
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=50)
    
    def __str__(self):
        return self.name

class BlogModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='タイトル')
    body = models.TextField(verbose_name='本文')
    thumbnail = models.ImageField(verbose_name='サムネイル', default='static/noimage.png',upload_to='static/') # サムネイル用のフィールドを用意
    post_datetime = models.DateTimeField(default=timezone.now, verbose_name='投稿日時')
    # category = models.CharField(max_length=40, choices=category_of_choice, verbose_name='カテゴリー')
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT, null=True, blank=True)
    # tag = models.CharField(max_length=40, choices=tag_of_choice, verbose_name='タグ')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    
    def __str__(self):
        return self.title