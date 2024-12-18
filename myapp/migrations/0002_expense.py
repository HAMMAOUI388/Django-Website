# Generated by Django 5.1.2 on 2024-12-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                ("category", models.CharField(max_length=100)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField(auto_now_add=True)),
            ],
        ),
    ]
