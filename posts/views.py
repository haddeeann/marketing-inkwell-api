from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils.text import slugify
import bleach
from rest_framework.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()

        if post.author != request.user:
            raise PermissionDenied("You can only publish your own posts.")

        post.published = True
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        post = self.get_object()

        if post.author != request.user:
            raise PermissionDenied("You can only unpublish your own posts.")

        post.published = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[])
    def published(self, *args, **kwargs):
        posts = Post.objects.filter(published=True).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def get_object(self):
        obj = super().get_object()
        if obj.published:
            return obj
        user = self.request.user
        if user.is_authenticated and obj.author == user:
            return obj

        raise PermissionDenied("You do not have permission to view this post.")

    # list / retrieve
    def get_queryset(self):
        qs = Post.objects.all().order_by("-created_at")
        author = self.request.query_params.get("author")

        if author:
            qs = qs.filter(author_id=author)

        # Anonymous users only see published
        if not self.request.user.is_authenticated:
            qs = qs.filter(published=True)
        return qs

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You can only delete your own posts.")
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        clean_html = bleach.clean(
            self.request.data.get("content", ""),
            tags=[
                "p", "strong", "em", "h1", "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "code", "pre", "br",
            ],
            attributes={},
            strip=True,
        )
        # Assign the logged-in user to the note
        serializer.save(author=self.request.user, content=clean_html, slug=slugify(self.request.data.get('title', '')))
