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
        form = GuessForm()
        return render(request, 'game.html', {'word': word, 'form': form})

    def post(self, request):
        # Get the most recent word from the database
        word = getWord()

        guess = request.POST.get('guess', '')

        if not word:
            error_message = "No words found in the database. Please add some words before playing the game."
            return render(request, 'game.html', {'error_message': error_message})


        similarity = cor(guess, word.word) if guess else None

        # Save the user's guess and confidence score to the database
        Guess.objects.create(
            word=word,
            guess=guess,
            similarity=similarity
        )

        # Redirect to the same page to display the result
        return redirect(reverse('game'))