import random
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Word
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
    guess_tokens = nltk.word_tokenize(guess.lower())
    answer_tokens = nltk.word_tokenize(answer.lower())
    guess_pos = nltk.pos_tag(guess_tokens)
    answer_pos = nltk.pos_tag(answer_tokens)
    try:
        guess_lemmas = [nltk.WordNetLemmatizer().lemmatize(t[0], pos=t[1][0].lower()) for t in guess_pos]
        answer_lemmas = [nltk.WordNetLemmatizer().lemmatize(t[0], pos=t[1][0].lower()) for t in answer_pos]
    except KeyError:
        guess_lemmas = [nltk.WordNetLemmatizer().lemmatize(t[0]) for t in guess_pos]
        answer_lemmas = [nltk.WordNetLemmatizer().lemmatize(t[0]) for t in answer_pos]
    guess_synsets = []
    for l in guess_lemmas:
        synsets = nltk.corpus.wordnet.synsets(l)
        if synsets:
            guess_synsets.append(synsets[0])

    answer_synsets = []
    for l in answer_lemmas:
        synsets = nltk.corpus.wordnet.synsets(l)
        if synsets:
            answer_synsets.append(synsets[0])
    sim_score = 0
    if guess_synsets and answer_synsets:
        sim_scores = [s1.path_similarity(s2) for s1 in guess_synsets for s2 in answer_synsets]
        sim_score = sum(sim_scores) / len(sim_scores)
        return [round(sim_score, 3), answer_synsets[0].definition().capitalize()]
    return [round(sim_score, 3), None]