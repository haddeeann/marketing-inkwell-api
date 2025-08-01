from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

