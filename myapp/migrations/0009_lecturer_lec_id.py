# Generated by Django 4.2.5 on 2024-04-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0008_remove_lecturer_lec_id_lecturer_assessees_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturer",
            name="lec_id",
            field=models.CharField(default="test", max_length=255),
            preserve_default=False,
        ),
    ]
