# api/uploads.py
import uuid
import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]  # adjust as needed

    def post(self, request):
        f = request.FILES.get('image')
        if not f:
            return Response({"error": "No file"}, status=400)
        if not f.content_type.startswith('image/'):
            return Response({"error": "Only images allowed"}, status=400)
        if f.size > 10 * 1024 * 1024:  # 10MB cap
            return Response({"error": "File too large"}, status=400)

        user_id = getattr(request.user, "id", "anon")
        key = f"uploads/{user_id}/{uuid.uuid4()}-{f.name}"

        s3 = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        extra = {
            "ContentType": f.content_type,
            "ServerSideEncryption": "AES256",
        }
        # If you insist on public S3 objects (simplest), uncomment next line.
        # Better: private bucket + CloudFront OAC.
        # extra["ACL"] = "public-read"

        s3.upload_fileobj(f, settings.AWS_S3_BUCKET, key, ExtraArgs=extra)

        if settings.CDN_PUBLIC_BASE_URL:
            url = f"{settings.CDN_PUBLIC_BASE_URL}/{key}"
        else:
            region = settings.AWS_S3_REGION
            url = f"https://{settings.AWS_S3_BUCKET}.s3.{region}.amazonaws.com/{key}"

        return Response({"url": url, "key": key})
