# Generated by Django 4.1.7 on 2023-04-01 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_remove_word_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guess',
            name='user',
        ),
    ]