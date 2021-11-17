#!/usr/bin/python3
import random
import re
import string

wordslist = ['blah blah', 'appendectomy', 'vasectomy', 'pronation', "poop 123"]
MAX_NUMBER_OF_GUESSES = 5

def generate_words(wordslist):
    random.shuffle(wordslist)
    for word in wordslist:
        yield word


# Regexes saying how to replace stuff
sanitizer = re.compile('[^a-zA-Z]+')
underscorer = re.compile('[a-zA-Z]')

'''
Remove anything that's not a character from the word.
'''
def characters_in_word(word):
    sanitized = sanitizer.sub('', word)
    output = set()
    for char in sanitized:
        output.add(char)
    return output

def underscore(word: string, guessed):
    built = word
    for idx, char in enumerate(word):
        if char not in guessed and underscorer.match(char):
            built = built[:idx] + "_" + built[idx+1:]
    return built


def get_a_guess(guessed):
    letter = None
    has_guessed = False
    while not letter or letter in guessed or len(letter) > 1:
        if has_guessed:
            print("Invalid entry!  Just enter an unguessed letter.")
        print("Guessed: [" + str(guessed) + "]")
        letter = input("Guess a letter: ")
        has_guessed = True

    return letter


def hangman(guesses):
    if guesses > 4:
        return '''    /-\\
               |   |xx|
                -------
                   \  |  /
                    \|/ 
                    /  \\'''
    elif guesses > 3:
        return '''    /-\\
               |   |xx|
                -------
                   \  |  /
                    \|/ 
                      \\'''
    elif guesses > 2:
        return '''    /-\\
               |   |xx|
                -------
                   \  |  /
                    \|/ 
                      '''
    elif guesses > 1:
        return '''    
               |  
                -------
                   \  |  /
                    \|/ 
                      '''
    elif guesses > 0:
        return '''    
                 |  
                  -------
                     \  | /
                      \|/
                        '''
    else:
        return ''' |
                    -----'''

def game_status(guessed, characters):
    bad_guesses = 0
    valid_guesses = set()
    for character in guessed:
        if character not in characters:
            bad_guesses = bad_guesses + 1
        else:
            valid_guesses.add(character)

    if bad_guesses > MAX_NUMBER_OF_GUESSES:
        print("You lose!  Next word.")
        return bad_guesses, True

    if valid_guesses == characters:
        print("You win!  Next word.")
        return bad_guesses, True

    return bad_guesses, False

def game():
    print("Welcome to hangman!")
    for word in generate_words(wordslist):
        characters = characters_in_word(word)
        guessed = set()
        bad_guesses = 0
        game_complete = False
        while not game_complete:
            print(underscore(word, guessed))
            print(hangman(bad_guesses))
            guess = get_a_guess(guessed)
            guessed.add(guess)
            bad_guesses, game_complete = game_status(guessed, characters)

if __name__ == '__main__':
    game()

