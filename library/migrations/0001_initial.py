# Generated by Django 3.2.12 on 2022-12-24 00:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("summary", models.TextField()),
                ("author", models.CharField(max_length=100)),
                ("cover", models.ImageField(blank=True, null=True, upload_to="")),
                ("number", models.IntegerField(default=0, verbose_name="Book number")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-modified"],
            },
        ),
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_borrowed", models.DateTimeField(auto_now_add=True)),
                ("date_return", models.DateTimeField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.book"
                    ),
                ),
            ],
            options={
                "ordering": ["-date_borrowed"],
            },
        ),
    ]
