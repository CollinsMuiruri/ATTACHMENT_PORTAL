# Generated by Django 4.2.5 on 2024-04-16 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("myapp", "0012_remove_student_assessor_remove_student_att_form_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lecturer",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("lec_id", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("assessor_status", models.BooleanField(default=False)),
                ("courses", models.ManyToManyField(to="myapp.course")),
            ],
        ),
    ]