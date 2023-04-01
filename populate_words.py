import os
import json

directory = '.'

filenames = ['nounlist.txt'] # Add more here if neccessary.

words = []
for filename in filenames:
    with open(os.path.join(directory, filename), 'r') as f:
        for line in f:
            words.append({'model': 'game.word', 'fields': {'word': line.strip()}})

with open('words.json', 'w') as f:
    json.dump(words, f)