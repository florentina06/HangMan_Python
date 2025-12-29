''' ---------------------------------- Random Words API ----------------------------------

    Role/ Purpose:
        Handles interaction with the random words API, providing words, categories, and languages.

    Main functions:
        - get_categories_languages() -> returns available languages and categories from the API.
        - get_valid_response(url) -> helper that checks API response for validity
        - get_random_word(language, category) → returns a random word for a given language and category.

    Used:
        - https://random-words-api.kushcreates.com/?utm_source=chatgpt.com
        - pip install requests - package to help me call the api

    Definitions:
        - API = Application Program Interface
        - jason = javascript object notation -> json a common way to pass data between 2 different programs (api and python script)

    Summary:
        Provides the data layer for the Hangman game. No user interaction or game logic here.  '''


import requests
import random


# ---------------------------------------------------------------------------
# Function: get_categories_languages
# ---------------------------------------------------------------------------
def get_categories_languages():
    ''' It returns two lists (languages and categories) with the available options.
        Notes:
            - The API returns a list of dictionaries with keys: word, length, category, language.
            - This function ensures that the returned lists contain unique values only. '''

    response = requests.get('https://random-words-api.kushcreates.com/api')
    response = response.json()              # It is a list of dictionaries; For example, response[1000] = a dictionary with the following keys: word, length, category, language; response[1000]['word'] = a word
    categories = []                         # I’m listing all existing categories here
    languages = []                          # I’m listing all existing languages here

    for item in response:                   # item = dictionary
        for key, value in item.items():
            if key == 'category':
                if value in categories:
                    continue
                else:
                    categories.append(value)

            if key == 'language':
                if value in languages:
                    continue
                else:
                    languages.append(value)

    return languages, categories



# ---------------------------------------------------------------------------
# Function: get_valid_response
# ---------------------------------------------------------------------------
def get_valid_response(url:str):
    '''Returns valid API data or raises a ValueError if the language – category combination does not exist.'''
    response = requests.get(url).json()

    if response is None:                   # API returns None when the combination doesn't exist
        raise ValueError("\nThis combination does not exist. You can try again.")
    else:
        return response



# ---------------------------------------------------------------------------
# Function: get_random_word
# ---------------------------------------------------------------------------
def get_random_word(language:str, category:str):
    '''Builds URL, checks validity, extracts words, returns a random one for the specified language and category.'''
    target = f'https://random-words-api.kushcreates.com/api?language={language}&category={category}'

    try:
        response = get_valid_response(target)
    except ValueError as err:
        raise err
    except Exception:
        raise Exception("Unexpected API error.")

    words = []
    for item in response:
        words.append(item['word'])

    return random.choice(words)



# ---------------------------------------------------------------------------
# Main execution for testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    languages, categories = get_categories_languages()
    print(languages, categories, sep = '\n')
    print(get_random_word('en', 'animals'))




