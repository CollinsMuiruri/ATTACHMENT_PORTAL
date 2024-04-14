# Generated by Django 4.2.5 on 2024-04-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0005_alter_student_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_type",
            field=models.CharField(
                choices=[
                    ("Self Sponsored Student", "Self Sponsored Student"),
                    ("Government Sponsored Student", "GSS"),
                ],
                default="Self Sponsored Student",
                max_length=255,
            ),
        ),
    ]