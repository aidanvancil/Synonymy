from django.contrib import admin
from .models import Word, Guess

class WordAdmin(admin.ModelAdmin):
    pass

class GuessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Word, WordAdmin)
admin.site.register(Guess, GuessAdmin)

