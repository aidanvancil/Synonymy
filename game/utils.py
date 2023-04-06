import random
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Word, Hint
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import nltk
import gensim.downloader as api
import math

model = api.load("glove-twitter-25")

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
    used_words = cache.get('usedWords', set())
    word = random.choice(words)
    english_set = frozenset(nltk.corpus.words.words())
    while word in used_words or len(word.word) > 9 or word.word not in english_set:
        word = random.choice(words)

    # Store the selected word in the cache with an expiration time set to the end of the day
    tomorrow = today + timedelta(days=1)
    end_of_day = datetime.combine(tomorrow, datetime.min.time())
    cache.set(f'getWord{today}', word, (end_of_day - datetime.now()).seconds)
    used_words.add(word.word)
    cache.set('usedWords', used_words)
    return word

def correlation(guess, answer):
    answer_synset = wn.synsets(answer)
    cosine_distance = model.similarity(guess, answer)
    cosine_distance = float(cosine_distance)
    try: 
        if not answer_synset[0]:
            return [round(cosine_distance, 3), None]
    except IndexError:
        return [round(cosine_distance, 3), "No definition"]
    return [round(cosine_distance, 3), answer_synset[0].definition().capitalize()]

def getRelevantWords(answer):
    similar_words = model.most_similar(answer, topn=15)
    for word, sim in similar_words:
        sim_score, definition = correlation(answer, word)
        if Hint.objects.count() > 3:
            break
        if definition is None or definition is "No definition":
            continue
        Hint.objects.create(
            word=word.title(),
            similarity=sim_score,
            definition=definition,
        )
    return