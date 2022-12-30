from rest_framework import serializers

from library.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    availability_stock = serializers.SerializerMethodField()

    def get_availability_stock(self, obj):
        availability = (
            obj.number
            - Borrowing.objects.filter(date_return__isnull=True, book=obj).count()
        )
        return availability

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "summary",
            "author",
            "cover",
            "number",
            "availability_stock",
            "created",
            "modified",
        )
        read_only_fields = ("id", "created", "modified")


class LibrarianBookSerializer(BookSerializer):
    availability_stock = serializers.SerializerMethodField()

    def get_availability_stock(self, obj):
        availability = (
            obj.number
            - Borrowing.objects.filter(date_return__isnull=True, book=obj).count()
        )
        return availability

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
