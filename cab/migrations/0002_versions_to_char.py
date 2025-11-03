from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cab", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snippet",
            name="version",
            field=models.CharField(
                max_length=5,
                default="0",
                choices=[
                    ("1.10", "1.10"),
                    ("1.9", "1.9"),
                    ("1.8", "1.8"),
                    ("1.7", "1.7"),
                    ("1.6", "1.6"),
                    ("1.5", "1.5"),
                    ("1.4", "1.4"),
                    ("1.3", "1.3"),
                    ("1.2", "1.2"),
                    ("1.1", "1.1"),
                    ("1.0", "1.0"),
                    ("0.96", ".96"),
                    ("0.95", "Pre .96"),
                    ("0", "Not specified"),
                ],
            ),
        ),
    ]
