import difflib
import random
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Word

def getWord():
    # Check if the word for today is already in the cache
    today = datetime.now().date()
    word = cache.get(f'getWord{today}')
    if word:
        return word

    # If the word for today is not in the cache, select a new random word from the database
    words = Word.objects.all()
    word = random.choice(words)

    # Store the selected word in the cache with an expiration time set to the end of the day
    tomorrow = today + timedelta(days=1)
    end_of_day = datetime.combine(tomorrow, datetime.min.time())
    cache.set(f'getWord{today}', word, (end_of_day - datetime.now()).seconds)

    return word

def cor(guess, answer):
    return difflib.SequenceMatcher(None, guess, answer).ratio()

