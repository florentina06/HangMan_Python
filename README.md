# 2_HangMan_Python

Project Description:
I created a Hangman game with a Tkinter graphical interface, where the user can choose the language and the word category through an API.

The project is structured into three files:

1. API file:
- Connects the game to an API that generates words based on the selected language and category
- Contains three main functions:
    - get_categories_languages() – returns all available languages and categories as lists
    - get_valid_response(url) – handles errors when the selected language–category combination does not exist
    - get_random_word(language, category) – generates a random word based on the user’s selection

2. Hangman file:
- Manages the Hangman game logic
- Contains:
    - A dictionary with the hangman stages for each mistake
    - The display_hangman(stage) function, which displays the hangman progress based on the number of mistakes
    - A HangMan class that contains multiple methods and the core game logic

3. Main file:
- Integrates the game logic with the Tkinter graphical interface
- The DisplayHangMan class controls windows, buttons, images, and the hangman display
- The play_game() method initializes the game screen, configures lives, the canvas, and the letter input field
- The play_hangman() method handles letter guessing, updates the word display, shows the hangman stages, and checks for win or loss conditions

This project combines external API usage, object-oriented programming, error handling, and a graphical user interface.
