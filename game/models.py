from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    word = models.CharField(max_length=100)
    hint = models.CharField(max_length=255, blank=True)
    explanation = models.TextField(blank=True)

class Guess(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    guess = models.CharField(max_length=100)
    similarity = models.FloatField()
    definition = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-similarity']

class Hint(models.Model):
    word = models.CharField(max_length=100)
    similarity = models.FloatField()
    definition = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-word']