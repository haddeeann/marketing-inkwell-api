import uuid
from django.db import models
from django.conf import settings


class MediaAsset(models.Model):
    """
    Stores one uploaded media file (right now: images for blog posts).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="media_assets",
    )

    # S3 key like: uploads/<user_id>/<uuid>-filename.jpg
    key = models.CharField(max_length=500, unique=True)

    # Convenience URL at time of upload (S3 or CDN)
    url = models.URLField(max_length=1000)

    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    # Optional alt text for accessibility / SEO
    alt_text = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_name} ({self.key})"
