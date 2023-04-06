from django.shortcuts import render, redirect, reverse
from game.models import Word, Guess, Hint
from game.forms import GuessForm
from django.http import HttpResponse
from django.views.generic import View
from game.utils import correlation, getWord, loadWords, getRelevantWords

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

    def get(self, request):
        guesses = Guess.objects.all()
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
                guesses = Guess.objects.all()
                hints = Hint.objects.all()
                form = GuessForm()
                return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': hints, 'error_message': error_message})
            else:
                error_message = "This word has already been guessed."
                guesses = Guess.objects.all()
                hints = Hint.objects.all()
                for obj in guesses:
                    if obj.guess.lower() == guess:
                        form = GuessForm()
                        return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': hints, 'error_message': error_message})

            sim_score, definition = correlation(guess, word.word)

            if sim_score != 1:
                definition = None
            else:
                answered = True

            Guess.objects.create(
                word=word,
                guess=guess.capitalize(),
                similarity=sim_score,
                definition=definition,
            )

        else:
            getRelevantWords(word.word)
            form = GuessForm()
            guesses = Guess.objects.all()
            hints = Hint.objects.all()

            return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses, 'hints': hints})
            
        return redirect(reverse(''))