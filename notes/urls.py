from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'', NoteViewSet, basename='note')  # so it's just /api/notes/

urlpatterns = [
    path('', include(router.urls)),
]
