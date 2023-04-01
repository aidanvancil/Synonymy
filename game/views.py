from django.shortcuts import render, redirect, reverse
from game.models import Word, Guess
from game.forms import GuessForm
from django.http import HttpResponse
from django.views.generic import View
from game.utils import cor, getWord, loadWords
import nltk

WORDS = loadWords()
word = getWord()

try:
    Guess.objects.all().delete()
except:
    pass

class GameView(View):
    def __init__(self, *args, **kwargs):
        super(GameView, self).__init__(*args, **kwargs)

    def getRelevantWords(self, answer):
        relevant_words = []
        for word in WORDS:
            sim_score, definition = cor(guess, answer)
            if sim_score > 0.3:
                relevant_words.append((guess, sim_score, definition))
        relevant_words = sorted(relevant_words, key=lambda x: x[1], reverse=True)
        return relevant_words

    def get(self, request):
        guesses = Guess.objects.filter(word=word)
        form = GuessForm()
        return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses})

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
            relevant_words = self.getRelevantWords(word.word)
            return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': relevant_words})
            
        return redirect(reverse(''))