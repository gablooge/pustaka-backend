from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
        return "{}: {}".format(self.id, self.title)
