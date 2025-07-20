from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        EDITOR = "editor", "Editor"
        WRITER = "writer", "Writer"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.WRITER,
    )
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_editor(self):
        return self.role == self.Role.EDITOR

    def is_writer(self):
        return self.role == self.Role.WRITER

    def __str__(self):
        return self.username
