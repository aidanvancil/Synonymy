# Generated by Django 4.1.7 on 2023-04-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_guess_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='guess',
            name='definition',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
