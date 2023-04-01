from django.contrib import admin
from .models import Word

class WordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Word, WordAdmin)
