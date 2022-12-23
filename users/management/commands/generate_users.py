from django.core.management.base import BaseCommand

from users.models import User


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cprint(text, color=None):
    if color:
        print(color + text + Colors.END)
    else:
        print(text)


class Command(BaseCommand):
    help = "Generate initial data"

    def handle(self, *args, **kwargs):
        cprint("Hello! We are going to create a librarian data.", Colors.BOLD)
        librarian = User(
            first_name="Samsul",
            last_name="Hadi",
        )
        email = "samsulhadikediri@gmail.com"
        password = "samlus"
        librarian.username = email
        librarian.email = email
        librarian.role = User.UserTypes.LIBRARIAN
        librarian.save()
        librarian.set_password(password)
        librarian.save()
        print(f"Created {librarian!r} for all this data!")

        student = User.objects.create(email="student@gmail.com")
        student.username = "student"
        student.role = User.UserTypes.STUDENT
        student.set_password("student")
        student.save()
        print(f"Created {student!r} for all this data!")
