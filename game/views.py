from django.shortcuts import render, redirect, reverse
from game.models import Word, Guess
from game.forms import GuessForm
from django.http import HttpResponse
from django.views.generic import View
from game.utils import cor, getWord

class GameView(View):
    def get(self, request):
        # Get the most recent word from the database
        word = getWord()
        guesses = Guess.objects.filter(word=word)
        form = GuessForm()
        return render(request, 'game.html', {'word': word, 'form': form, 'guesses': guesses})

    def post(self, request):
        # Get the most recent word from the database
        word = getWord()

        guess = request.POST.get('guess', '')

        if not word:
            error_message = "No words found in the database. Please add some words before playing the game."
            return render(request, 'game.html', {'error_message': error_message})

        print(guess)
        if guess and guess not in [w.word for w in Word.objects.all()]:
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

        similarity = cor(guess, word.word) if guess else None
        
        Guess.objects.create(
            word=word,
            guess=guess,
            similarity=similarity
        )

        return redirect(reverse(''))