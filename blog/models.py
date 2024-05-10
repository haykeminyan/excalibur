from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(choices=[('politics', 'Politics'), ('history', 'History'), ('sport', 'Sport')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        'auth.User',
        related_name='blogs',
        on_delete=models.CASCADE,
        null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs_by_category')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(choices=[('hy', 'HY'), ('en', 'EN'), ('ru', 'RU'), ('es', 'ES'), ('pt', 'PT')])

    def __str__(self):
        return f"Blog by {self.author} - Category: {self.category}, Language: {self.language}"