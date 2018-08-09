from django.db import models


class userinfo(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()