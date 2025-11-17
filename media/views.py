import uuid
import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import MediaAsset


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        f = request.FILES.get('image')
        if not f:
            return Response({"error": "No file"}, status=status.HTTP_400_BAD_REQUEST)
        if not f.content_type.startswith('image/'):
            return Response({"error": "Only images allowed"}, status=status.HTTP_400_BAD_REQUEST)
        if f.size > 10 * 1024 * 1024:
            return Response({"error": "File too large"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_id = getattr(user, "id", "anon")
        key = f"uploads/{user_id}/{uuid.uuid4()}-{f.name}"

        s3 = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        extra = {
            "ContentType": f.content_type,
            "CacheControl": "public, max-age=31536000, immutable",
            "ServerSideEncryption": "AES256",
        }

        s3.upload_fileobj(f, settings.AWS_S3_BUCKET, key, ExtraArgs=extra)

        # Build the public URL (S3 for now, CDN later)
        region = settings.AWS_S3_REGION
        url = f"{settings.CDN_PUBLIC_BASE_URL}.s3.{region}.amazonaws.com/{key}"

        asset = MediaAsset.objects.create(
            owner=user,
            key=key,
            url=url,
            original_name=f.name,
            content_type=f.content_type,
            size_bytes=f.size,
        )

        # Keep existing frontend contract: { url, key }
        # But also return an id for future features
        return Response(
            {
                "id": str(asset.id),
                "url": asset.url,
                "key": asset.key,
                "alt": asset.alt_text,
            },
            status=status.HTTP_201_CREATED,
        )
