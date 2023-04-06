# Synonymy

## Description

This project is a game where the user has to guess a word based on the semantic-similarity of their guesses.
![hotstreak](https://user-images.githubusercontent.com/42700427/230251342-5cd18544-3a99-4373-a20e-5462a4012085.jpg)

## Technologies Used

- Django
- NLTK, Gensim, Word2Vec


## How to Play

1. The user is allowed to make as many guesses as they wish until they go into an infernal rage.
2. The user must try to guess the daily word through guesses.
3. If the user enters the correct word, a success message is displayed.
4. If the user enters an incorrect word, a message is displayed letting them know and they can try again.
5. If the user is stuck, they can request a hint which will provide relevant words that relate to the daily word.

## Installation (For Contributions)

1. Clone the repository to your local machine.
2. Install Python and Django if they are not already installed (see requirements.txt).
3. In root directory use the following command: `pip install -r requirements.txt`.
4. Open a terminal and navigate to the project directory.
5. Run the command `python manage.py runserver`.
6. Open a web browser and navigate to `http://localhost:8000/` to start playing the game.

## Additional Features

- The game provides a hint feature to help users who are stuck.

![hints](https://user-images.githubusercontent.com/42700427/230251336-1b26ca8b-fe40-42ad-b087-f93ab601068c.jpg)


## Future Improvements

- Implement a multiplayer feature where users can compete against each other.
- Add additional difficulty levels with harder definitions.
- Allow users to submit their own definitions and words for the game.

