''' ------------------------------- HangMan GUI -------------------------------

    Role / Purpose:
        Provides a graphical user interface for the Hangman game using Tkinter.
        Handles screen transitions, user input, button interactions, and visual
        feedback (ASCII hangman rendering, word progress, lives, and hints).

    Contains:
       - class DisplayHangMann → main GUI controller:
            __init__()                        → initializes window, UI placeholders, and start screen.
            - create_spider_image()             → loads and displays top spider image.
            - create_hangman_title()            → creates title label for start screen.
            - hide_hangman_title()              → hides the title element.
            - create_start_button()             → places the start button on screen.
            - hide_start_button()               → hides the start button.
            - language_category()               → builds dropdown UI for language & category selection.
            - hide_language_category()          → hides selection screen elements.
            - get_choosen_word()                → retrieves a random word based on user selection.
            - play_game()                       → initializes game UI elements and HangMan logic.
            - create_hangman_image()            → displays start screen hangman image.
            - hide_hangman_image()              → hides hangman image from start screen.
            - display_hangman_on_canvas(stage)  → draws ASCII hangman on Tkinter canvas.
            - play_hangman()                    → handles guess logic, validation, updates UI, win/lose state.
            - back_to_menu()                    → clears game screen and returns to selection menu.
            - run()                             → starts the Tkinter main loop.

    External Dependencies:
        - api.get_categories_languages       → returns available languages and word categories.
        - api.get_random_word                → returns a random word given language & category.
        - hangman.HangMan                    → game logic class (state, guess validation, win/lose rules).
        - hangman.display_hangman            → returns ASCII hangman figure by stage.
        - hangman.hangman                    → dictionary of ASCII hangman stages.

    Summary:
        This module manages the full GUI for a Hangman game workflow:
        - start screen → category selection → gameplay UI.
        - Updates game visuals dynamically and integrates core HangMan logic
        - with Tkinter widgets, canvas drawing, buttons, and message dialogs.

    Colors:
        - #00FF00 - verde
        - #FF5500 - portocaliu
        - #000000 - negru '''


import tkinter as tk
from tkinter import PhotoImage, messagebox   # importa pentru poze si fereastra de mesaje
from api import get_categories_languages, get_random_word
from hangman import display_hangman, hangman, HangMan


class DisplayHangMann:
    def __init__(self):
        # ---------------------------------------------------------------------------
        # Configure main window
        # ---------------------------------------------------------------------------
        self.window = tk.Tk()                                       # Create window instance
        self.window.geometry( "600x900" )                           # Default window size
        self.window.title( 'HangMan' )                              # Window title
        self.window.config( background="black", cursor="pirate" )   # Styling + fun cursor


        # ---------------------------------------------------------------------------
        # App icon (spider logo in title bar)
        # ---------------------------------------------------------------------------
        self.logo = PhotoImage( file="images//spider.png" )         # Convert the image to a photo format
        self.window.iconphoto(True, self.logo)               # Add the logo to my window.


        # ---------------------------------------------------------------------------
        # Build initial UI (start screen)
        # ---------------------------------------------------------------------------
        self.create_spider_image()
        self.create_hangman_title()
        self.create_start_button()
        self.create_hangman_image()


        # ---------------------------------------------------------------------------
        # DEBUG ONLY — shows chosen word (remove later)
        # ---------------------------------------------------------------------------
        self.word_label = tk.Label( self.window, text='', font=('Chiller', 20, 'bold'), fg='#FF5500', bg='black' )
        self.word_label.pack( pady=10 )


    # -------------------------------------------------------------------------
    # 1. START SCREEN (visible at application launch)
    # -------------------------------------------------------------------------
    def create_spider_image(self):
        ''' Displays the top spider graphic (persistent element across screens) '''
        self.spider_image = PhotoImage( file='images\\spider (4).png' )
        self.spider_label = tk.Label( self.window, image = self.spider_image, compound='top', bg="black" )
        self.spider_label.pack( side='top' )

    def create_hangman_title(self):
        ''' Creates and displays the main HangMan title on the start screen.'''
        self.spider_small = tk.PhotoImage( file = 'images\\spider (1).png')
        self.title_label = tk.Label(
            self.window, text = "HangMan Game", font = ('Chiller',40,'bold'), fg = '#00FF00',   # fg = font color
            bg = "black", padx = 20, pady = 10, image = self.spider_small, compound = 'right' ) # bk = background color, padx = padding on the X-axis, pady = padding on the Y-axis
        self.title_label.pack()                                                                 # add the label to the window

    def hide_hangman_title(self):
        ''' Hides the HangMan title label (used when switching screens). '''
        if self.title_label:
            self.title_label.pack_forget()

    def create_start_button(self):
        ''' Creates the "Start" button and links it to language/category screen.'''
        self.start_button = tk.Button(
            self.window, text = 'Start', font = ('Chiller',30,'bold'), fg = '#FF5500',
            bg = "black", activebackground = "#FF5500", activeforeground = '#000000',           # activebackground = button color when pressed, activeforeground = text color when the button is pressed
            padx = 20, pady = 10, command = self.language_category, cursor = 'hand2')
        self.start_button.pack( pady=30 )

    def hide_start_button(self):
        ''' Hides the start button. '''
        if self.start_button:
            self.start_button.pack_forget()


    # -------------------------------------------------------------------------
    # 2. SELECTION SCREEN
    # -------------------------------------------------------------------------
    def language_category(self):
        ''' Displays the language and category selection screen.
            - Hides the main start screen widgets (title, start button, initial hangman image).
            - Loads languages and categories from the API.
            - Builds dropdowns for user selection.
            - Adds "Play" button to proceed to the game.'''

        # ---------------------- Hide main screen widgets ----------------------
        self.hide_hangman_title()
        self.hide_start_button()
        self.hangman_image.pack_forget()                             # Close the image so I can reopen it and have it appear at the bottom.

        # ---------------------- Fetch available languages and categories from API ----------------------
        languages, categories = get_categories_languages()

        # ---------------------- Create a frame to hold dropdowns and play button ----------------------
        self.selection_frame = tk.Frame( self.window, bg='black' )
        self.selection_frame.pack( pady=20 ) # spatiu fata de sus

        # ---------------------- Language dropdown ----------------------
        self.language_var = tk.StringVar( value="Choose language" )                                      # Create a Tkinter variable to store the selected value in the language dropdown.
        self.language_menu = tk.OptionMenu( self.selection_frame, self.language_var,*languages )  # Create a dropdown menu (OptionMenu) in the 'window'; 'language_var' stores the selected value. '*languages' unpacks the 'languages' list as menu option
        self.language_menu.config(
            width=20, font = ('Chiller',16,'bold'),  fg = '#00FF00', bg = "black",
            highlightbackground='black', highlightcolor='#00FF00', bd=2, highlightthickness=0, activebackground = '#FF5500')
        self.language_menu.pack( side='left', pady=10 )
        self.language_menu['menu'].config( bg='#111111', fg='#00FF00', activebackground = '#FF5500', activeforeground = 'black', font = ('Arial', 10, 'bold') )  # Change the colors in the language menu.

        # ---------------------- Category dropdown ----------------------
        self.category_var = tk.StringVar( value='Choose your category' )
        self.category_menu = tk.OptionMenu( self.selection_frame, self.category_var, *categories )
        self.category_menu.config(
            width=20, font = ('Chiller',16,'bold'),  fg = '#00FF00', bg = "black",
            highlightbackground='black', highlightcolor='#00FF00', bd=2, highlightthickness=0, activebackground = '#FF5500')
        self.category_menu.pack( side='left', pady=10 )
        self.category_menu['menu'].config( bg='#111111', fg='#00FF00', activebackground = '#FF5500', activeforeground = 'black', font = ('Arial', 10, 'bold') )


        # ---------------------- Play button starts the game ----------------------
        self.play_button = tk.Button(
            self.window, text='Play', font = ('Chiller',30,'bold'), fg = '#FF5500', bg = 'black',
            activeforeground = '#FF5500', activebackground = '#000000',  padx = 20, pady = 10,
            command = self.play_game, cursor = 'hand2' )                                                                     # Start when I press play
        self.play_button.pack( pady=10 )

        # ---------------------- Show initial hangman image below ----------------------
        self.hangman_image.pack()


    def hide_language_category(self):
        ''' Hides the language/category selection screen widgets '''
        if self.selection_frame:
             self.selection_frame.pack_forget()
        if self.play_button:
            self.play_button.pack_forget()



    # -------------------------------------------------------------------------
    # 3. GET CHOSEN WORD
    # -------------------------------------------------------------------------
    def get_choosen_word(self):
        ''' Returns a random word selected based on user's language and category. '''
        self.word = get_random_word(self.language_var.get(), self.category_var.get())
        return self.word


    # -------------------------------------------------------------------------
    # 4. PLAY GAME (init UI joc + logic)
    # -------------------------------------------------------------------------
    def play_game(self):
        ''' Initializes the gameplay screen:
            - Hides previous screens
            - Sets up lives label, ASCII hangman canvas, word hint, input entry, guess button, and back button
            - Instantiates the HangMan logic class '''
        try:
            word = self.get_choosen_word()
            self.word_label.config( text = '' )             # clear error/debug messages
            # self.word_label.config( text = f'Start game with word: {word}', font=("Arial", 14, "bold"), fg = '#FF5500' ) # Display the word in a label for testing.
        except ValueError as err:
            self.word_label.config( text = f'Error! {err}', font=("Arial", 14, "bold"), fg = '#FF5500' )
            return
        except Exception as e:
            self.word_label.config( text = f'Unexpected error: {e}', font=("Arial", 14, "bold"), fg = '#FF5500' )
            return


        # ---------------------- Hide selection screen ----------------------
        self.hide_language_category()
        self.hide_hangman_image()

        # ---------------------- Lives label ----------------------
        self.lives_label = tk.Label(self.window, text = f'Lives Remaining: {len(hangman) - 1}', font=('Helvetica', 16), fg = '#FF5500', bg = 'black')
        self.lives_label.pack()

        # ---------------------- ASCII hangman canvas ----------------------
        self.canvas = tk.Canvas(self.window, width=200, height=200, bg='black', highlightthickness=0)
        self.canvas.pack( pady = 5 )

        # ---------------------- Guessed word progress label ----------------------
        self.guessed_word_label = tk.Label( self.window, text="_ " * len(word), font=("Helvetica", 20), fg = '#FF5500', bg = 'black' )
        self.guessed_word_label.pack( pady = 5 )

        # ---------------------- Entry field for guesses ----------------------
        self.entry_letter = tk.Entry( self.window, font = ("Helvetica", 16), bg = '#22241f', fg = "#00FF00" )
        self.entry_letter.pack( pady = 5 )  # Afișează câmpul

        # ---------------------- Guess button ----------------------
        self.guess_button = tk.Button(
            self.window, text = 'Guess', font=('Chiller', 20, 'bold'), fg='#FF5500', bg='black',
            activeforeground='#FF5500', activebackground='#000000', padx=10, pady=10, command = self.play_hangman, cursor = 'hand2' )
        self.guess_button.pack( pady = 5 )

        # ---------------------- Back button to return to selection screen ----------------------
        self.back_button = tk.Button(
            self.window, text = 'Back', font=('Chiller', 20, 'bold'), fg='#00FF00', bg='black',
            activeforeground='#FF5500', activebackground='#000000', padx=10, pady=10, command = self.back_to_menu )
        self.back_button.pack( pady = 5 )

        # ---------------------- Instantiate HangMan logic ----------------------
        self.game = HangMan( word )

        # ---------------------- Initialize hangman canvas stage ----------------------
        self.display_hangman_on_canvas(0)



    # -------------------------------------------------------------------------
    # 5. HANGMAN IMAGE
    # -------------------------------------------------------------------------
    def create_hangman_image(self):
        ''' Displays the initial Hangman image on the start screen. '''
        self.photo = PhotoImage( file='images\\Halloween_HangMan_small.png' )
        self.hangman_image = tk.Label( self.window, image = self.photo, bg="black", compound='bottom')
        self.hangman_image.pack()

    def hide_hangman_image(self):
        ''' Hides the initial hangman image '''
        if self.hangman_image:
            self.hangman_image.pack_forget()



    # -------------------------------------------------------------------------
    # 6. CANVAS + DISPLAY ASCII HANGMAN
    # -------------------------------------------------------------------------
    def display_hangman_on_canvas(self, stage:int):
        ''' Draws the ASCII hangman on the canvas according to the current stage.
            Args: stage (int) = The number of wrong guesses (hangman stage) '''

        # ---------------------- Clear previous drawing ----------------------
        self.canvas.delete('all')

        # ---------------------- Get ASCII lines for current stage ----------------------
        try:
            lines = display_hangman(stage)                                                 # Call the function from an external file; it receives the list of lines for this stage.
        except Exception as e:                                                             # If display_hangman doesn’t exist or raises an error, show a fallback.
            messagebox.showinfo("Error", str(e) )

        # ---------------------- Draw lines on canvas ----------------------
        y = 10                                                                             # Set the vertical coordinate y for the first line on the canvas.
        for line in lines:                                                                 # Iterate through each ASCII line returned by display_hangman.
            self.canvas.create_text(
                30, y, text=line, font=('Courier New', 15), anchor='nw', fill='#FF5500' )  # Write text on the canvas: 10 is the x-coordinate, y is the vertical coordinate, text = line is the text to display, anchor – the top-left corner of the text is placed at (x, y)
            y += 18                                                                        # The space between lines.



    # -------------------------------------------------------------------------
    # 7. PLAY HANGMAN (button logic)
    # -------------------------------------------------------------------------
    def play_hangman(self):
        ''' Handles the logic when the user clicks the Guess button:
            - Reads the input letter
            - Validates and updates HangMan logic
            - Updates guessed word, lives, and hangman canvas
            - Checks win/lose conditions
            - Offers hints after 3 consecutive wrong guesses '''

        guess = self.entry_letter.get()                                                    # Get the text entered in the entry (letter or word)
        self.entry_letter.delete( 0, "end" )                                     # Clear the entry’s content after reading


        # ---------------------- Attempt to make a guess using HangMan logic ----------------------
        try:
            self.game.make_guess(guess)                                                    # Submit the guess to the game logic.
        except ValueError as e:                                                            # If the user enters something invalid.
            messagebox.showinfo("Error", str(e))                                      # Display an error message
            return

        # ---------------------- Update displayed guessed word ----------------------
        self.guessed_word_label.config(text=" ".join(self.game.hint))                      # Update the displayed word (with guessed letters)

        # ---------------------- Update lives label ----------------------
        remaining_lives = len(hangman) - 1 - self.game.wrong_guesses
        self.lives_label.config( text = f'Lives Remaining: {remaining_lives}')             # Update the number of lives.


        # ---------------------- Update hangman canvas ----------------------
        self.display_hangman_on_canvas(self.game.wrong_guesses)                            # Draw the current stage of the hangman


        # ---------------------- Check for win condition ----------------------
        if "_" not in self.game.hint:                                                      # If there are no more "_" → the word is fully guessed.
            messagebox.showinfo("WIN", 'Congrats! You WON!')
            self.guess_button.config( state="disabled" )                                   # Disable the Check button
            return

        # ---------------------- Check for lose condition ----------------------
        if self.game.wrong_guesses >= len(hangman) - 1:                                    # If lives are exhausted.
            messagebox.showinfo("LOSE", f'You LOST! The word was {self.game.answer}')
            self.guess_button.config(state="disabled")                                     # Disable the Check button
            return  # mai am nevoie de return?


        # ----------------------  Hint logic: offer hint after 3 consecutive wrong guesses ----------------------
        if self.game.consecutive_errors == 3:
            ask = messagebox.askyesno("Hint", "Do you want a hint?")
            if ask:
                hint_msg = self.game.give_hint()                                            # Generate the hint
                messagebox.showinfo("Hint", hint_msg)
                self.guessed_word_label.config(text=" ".join(self.game.hint))
            self.game.consecutive_errors = 0                                                # Reset the count of consecutive mistakes


    # -------------------------------------------------------------------------
    # 8. BACK TO MENU
    # -------------------------------------------------------------------------
    def back_to_menu(self):
        ''' Returns to the selection menu by hiding gameplay widgets and reloading selection screen. '''

        # ----------------------  Hide all gameplay widgets ----------------------
        self.lives_label.pack_forget()
        self.canvas.pack_forget()
        self.guessed_word_label.pack_forget()
        self.entry_letter.pack_forget()
        self.guess_button.pack_forget()
        self.back_button.pack_forget()

        # ----------------------  Reload selection screen ----------------------
        self.language_category()


    # -------------------------------------------------------------------------
    # 9. RUN APPLICATION
    # -------------------------------------------------------------------------
    def run(self):
        ''' Starts the Tkinter main loop '''
        self.window.mainloop()



# ---------------------------------------------------------------------------
# MAIN EXECUTION (for testing)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = DisplayHangMann()
    app.run()











