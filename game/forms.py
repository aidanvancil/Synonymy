from django import forms

class GuessForm(forms.Form):
    guess = forms.CharField(label='Guess', max_length=100)