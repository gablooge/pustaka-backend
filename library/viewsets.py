from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer, LibrarianBookSerializer
from users.permissions import IsLibrarian, ReadOnly


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsLibrarian | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if not self.request.user.is_anonymous and self.request.user.is_librarian():
            return LibrarianBookSerializer
        else:
            return BookSerializer
