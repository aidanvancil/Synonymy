import random
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Word
from nltk.wsd import lesk
import nltk

def loadWords():
    WORDS = [w.word for w in Word.objects.all()]
    return WORDS

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
    guess_synset = lesk(guess, guess)
    answer_synset = lesk(answer, answer)
    if not guess_synset:
        return [0, 0]
    sim_score = (guess_synset.wup_similarity(answer_synset))
    
    return [round(sim_score, 3), answer_synset.definition().capitalize()]