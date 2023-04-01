from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    word = models.CharField(max_length=100)
    hint = models.CharField(max_length=255, blank=True)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Guess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    guess = models.CharField(max_length=100)
    similarity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-similarity']