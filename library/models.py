from django.db import models

from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    author = models.CharField(max_length=100)
    cover = models.ImageField(blank=True, null=True)
    number = models.IntegerField(verbose_name="Book number", default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified"]

    def __str__(self):
        return f"{self.id}:{self.title}"


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    date_return = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-date_borrowed"]

    def __str__(self):
        return f"{self.id}: Student {self.student.id}. {self.student.email} borrow {self.book.id}. {self.book.title}"
