from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class UserTypes(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        LIBRARIAN = "LIBRARIAN", "Librarian"

    role = models.CharField(
        max_length=10,
        choices=UserTypes.choices,
        default=UserTypes.STUDENT,
    )

    def is_librarian(self):
        return self.role == self.UserTypes.LIBRARIAN


class StudentManager(models.Manager):
    def get_queryset(self):
        return (
            super(StudentManager, self)
            .get_queryset()
            .filter(role=User.UserTypes.STUDENT)
        )


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = User.UserTypes.STUDENT
        return super(Student, self).save(*args, **kwargs)


class LibrarianManager(models.Manager):
    def get_queryset(self):
        return (
            super(LibrarianManager, self)
            .get_queryset()
            .filter(role=User.UserTypes.LIBRARIAN)
        )


class Librarian(User):
    objects = LibrarianManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = User.UserTypes.LIBRARIAN
        return super(Librarian, self).save(*args, **kwargs)
