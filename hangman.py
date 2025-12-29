''' ------------------------------- HangMan Logic -------------------------------

    Role / Purpose:
        Implements the Hangman game logic and provides ASCII visualizations.

    Contains:
       - hangman dict             → ASCII representations for each stage of wrong guesses.
       - display_hangman(stage)   → prints the hangman figure for a given stage.
       - class HangMan            → encapsulates the game state and logic:
            __init__(self, word)  → initializes the game with the chosen word.
            display_hint()        → shows current guessed letters.
            display_answer()      → returns the full answer.
            validate_input(guess) → checks if input is valid.
            make_guess(guess)     → updates game state based on guessed letter.
            give_hint()           → reveals a random letter from the remaining letters

    Summary:
        Provides an object-oriented implementation of Hangman with ASCII drawing support and user input validation. '''

import random


# ---------------------------------------------------------------------------
# ASCII Hangman Stages
#   Dictionary representing the hangman at each stage of wrong guesses.
#   Key = number of wrong guesses
#   Value = tuple of strings (head, body, legs)
# ---------------------------------------------------------------------------

hangman = {0: ("   ",
               "   ",
               "   "),
           1: (" o ",
               "   ",
               "   "),
           2: (" o ",
               " | ",
               "   "),
           3: (" o ",
               "/| ",
               "   "),
           4: (" o ",
               "/|\\",
               "   "),
           5: (" o ",
               "/|\\",
               "/  "),
           6: (" o ",
               "/|\\ ",
               "/ \\") }


def display_hangman(stage):
    '''Displays the hangman figure corresponding to the number of wrong guesses.
       The hangman is drawn progressively, showing head, body, arms, and legs based on mistakes.'''

    head, body, legs = hangman[stage]
    gallows = [
        " +------+ ",
        " |      |",
        " |     " + head,
        " |     " + body,
        " |     " + legs,
        " |     ",
        "_|_________",
    ]
    return gallows



# ---------------------------------------------------------------------------
# HangMan Game Class
# ---------------------------------------------------------------------------
class HangMan:
    ''' Encapsulates the Hangman game logic, state, and guess validation. '''
    def __init__(self, word:str):
        self.answer = word.lower()                                                   # store the answer in lowercase
        self.hint = [ char if not char.isalpha() else "_" for char in self.answer ]  # Create a list of underscores representing unguessed letters; spaces remain unchanged
        self.wrong_guesses = 0                                                       # count of incorrect guesses
        self.guessed_letters = set()                                                 # store guessed letters (no duplicates)
        self.consecutive_errors = 0                                                  # counts consecutive wrong guesses


    # ---------------------------------------------------------------------------
    # Display Methods
    # ---------------------------------------------------------------------------
    def display_hint(self):
        ''' Returns the current state of the guessed word as a string. '''
        return " ".join(self.hint)


    def display_answer(self):
        ''' Returns the full answer. '''
        return " ".join(self.answer)


    # ---------------------------------------------------------------------------
    # Input Validation
    # ---------------------------------------------------------------------------
    def validate_input(self, guess:str):
        ''' Validates the user's input for guessing.
            Args: guess (str): Input character.'''
        if len(guess) != 1:
            raise ValueError("You must enter exactly one letter.\n")

        if not guess.isalpha():
            raise ValueError("You must enter a letter.\n")

        if guess in self.guessed_letters:
            raise ValueError(f'"{guess}" was already guessed.\n')

        return guess


    # ---------------------------------------------------------------------------
    # Game Logic
    # ---------------------------------------------------------------------------
    def make_guess(self, guess:str):
        ''' Updates the game state based on a guessed letter: validates the input, adds it to guessed letters, reveals letters in the hint if correct, or increments wrong guesses if incorrect.
            Args: guess (str): Letter guessed by the player.'''
        guess = guess.lower()                  # Convert the input to lowercase
        guess = self.validate_input(guess)     # Validate the guess (single letter, alphabetic, not already guessed)
        self.guessed_letters.add(guess)        # Record the guessed letter in the set of guessed letters

        if guess in self.answer:               # if the guessed letter is present anywhere in the answer
            for i in range(len(self.answer)):  # loop over all indices of the answer string
                if self.answer[i] == guess:    # if the character at index i matches the guessed letter
                    self.hint[i] = guess       # reveal that letter in the hint at the same index
            self.consecutive_errors = 0        # reset because the user guessed correctly
        else:
            self.wrong_guesses += 1            # if the letter is not in the answer, increment wrong guesses
            self.consecutive_errors += 1


    def give_hint(self):
        ''' Provides a hint by revealing a random unguessed letter. '''
        unrevealed = []                        # Will contain the list of positions (indexes) where the word has not been guessed yet; the positions in self_hint where there is an "_"
        for i in range(len(self.hint)):
            if self.hint[i] == "_":
                unrevealed.append(i)

        if "_" not in self.hint:
            return "No hint needed, you already know the word."

        index = random.choice(unrevealed)
        self.hint[index] = self.answer[index]

        self.consecutive_errors = 0            # reset consecutive errors after hint

        return f"Hint: the letter '{self.answer[index]}' is in the word.\n"



