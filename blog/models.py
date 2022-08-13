from django.db import models
from django.utils import timezone

class BlogModel(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    post_datetime = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title