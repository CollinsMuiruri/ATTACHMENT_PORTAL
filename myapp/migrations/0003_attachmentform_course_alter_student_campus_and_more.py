# Generated by Django 4.2.5 on 2024-04-12 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_student_middle_name_alter_student_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttachmentForm",
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
                ("status", models.BooleanField(default=False)),
                ("organisation", models.CharField(max_length=255)),
                ("join_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name="student",
            name="campus",
            field=models.CharField(
                choices=[
                    ("MAIN CAMPUS", "MAIN CAMPUS"),
                    ("TOWN CAMPUS", "TOWN CAMPUS"),
                    ("WESTERN CAMPUS", "WESTERN CAMPUS"),
                    ("KITENGELA CAMPUS", "KITENGELA CAMPUS"),
                ],
                default="MAIN CAMPUS",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="study_mode",
            field=models.CharField(
                choices=[
                    ("FULL TIME", "FULL TIME"),
                    ("PART TIME", "PART TIME"),
                    ("DISTANCE LEARNING", "DISTANCE LEARNING"),
                ],
                default="FULL TIME",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="lecturer",
            name="courses",
            field=models.ManyToManyField(to="myapp.course"),
        ),
        migrations.AddField(
            model_name="student",
            name="att_form",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.attachmentform",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="myapp.course"
            ),
        ),
    ]