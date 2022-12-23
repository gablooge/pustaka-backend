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
