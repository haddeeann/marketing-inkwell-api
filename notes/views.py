from rest_framework import viewsets, permissions
from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return notes for the authenticated user
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the logged-in user to the note
        serializer.save(user=self.request.user)

