# Generated by Django 4.2.5 on 2024-04-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0004_student_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="email",
            field=models.EmailField(
                default="null_mail@students.kcau.ac.ke", max_length=254
            ),
            preserve_default=False,
        ),
    ]