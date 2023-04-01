from django.shortcuts import render, redirect, reverse
from game.models import Word, Guess, Hint
from game.forms import GuessForm
from django.http import HttpResponse
from django.views.generic import View
from game.utils import cor, getWord, loadWords
import nltk

WORDS = loadWords()
word = getWord()

try:
    Guess.objects.all().delete()
    Hint.objects.all().delete()
except:
    pass

class GameView(View):
    def __init__(self, *args, **kwargs):
        super(GameView, self).__init__(*args, **kwargs)

    def getRelevantWords(self, threshold = 0.3):
        synonyms = []
        known = []
        for syn in nltk.corpus.wordnet.synsets(word.word):
            for lemma in syn.lemmas():
                if lemma.name() not in known:
                    known.append(lemma.name())
                    if lemma.name() != word.word or word.word.find(lemma.name()) or lemma.name().find(word.word):
                        sim_score, definition = cor(word.word, lemma.name())
                        if Hint.objects.count() > 3:
                            break
                        Hint.objects.create(
                            word=lemma.name(),
                            similarity=sim_score,
                            definition=definition,
                        )
        return

    def get(self, request):
        guesses = Guess.objects.filter(word=word)
        hints = Hint.objects.all()
        form = GuessForm()
        return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': hints})

    def post(self, request):
        guess = request.POST.get('guess', '')
        guess = guess.lower()
        hint = request.POST.get('hint', '')
        if guess:
            if not word:
                error_message = "No words found in the database. Please add some words before playing the game."
                return render(request, 'game.html', {'error_message': error_message})

            if guess not in WORDS:
                error_message = "This word cannot be found."
                guesses = Guess.objects.filter(word=word)
                form = GuessForm()
                return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'error_message': error_message})
            else:
                error_message = "This word has already been guessed."
                guesses = Guess.objects.filter(word=word)
                for obj in guesses:
                    if obj.guess == guess:
                        form = GuessForm()
                        return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'error_message': error_message})

            sim_score, definition = cor(guess, word.word) if guess else [0, None]

            if sim_score != 1:
                definition = None

            Guess.objects.create(
                word=word,
                guess=guess.capitalize(),
                similarity=sim_score,
                definition=definition,
            )

        else:
            self.getRelevantWords()
            form = GuessForm()
            guesses = Guess.objects.filter(word=word)
            hints = Hint.objects.all()

            return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': hints})
            
        return redirect(reverse(''))