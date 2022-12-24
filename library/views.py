# from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Borrowing
from library.serializers import StudentBorrowBookSerializer
from users.models import Student
from users.permissions import IsLibrarian


# Create your views here.
class BorrowBookView(APIView):
    permission_classes = [
        IsLibrarian,
    ]

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def post(self, request, pk, *args, **kwargs):
        student = self.get_object(pk)
        serializer = StudentBorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        books = serializer.data.get("books")
        for book_id in books:
            Borrowing.objects.create(student=student, book_id=book_id)
        return Response(serializer.data)
