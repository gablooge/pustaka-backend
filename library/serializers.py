from rest_framework import serializers

from library.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "cover",
            "number",
            "created",
            "modified",
        )
        read_only_fields = ("id", "created", "modified")


class LibrarianBookSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "cover",
            "number",
            "created",
            "modified",
            "created_by",
        )
        read_only_fields = ("id", "created", "modified", "created_by")


class StudentBorrowBookSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = ("books",)
