'''
This module reproduce an offline version of Guess the Language from baltoslav.eu.

Functions
---------
.. autofunction:: guess_the_language

Exemples
--------
Assuming the module was imported as follow::

    >>> from baltoslav.ai import Languages
    >>> from baltoslav.game import guess_the_language

You first need a language database::

    >>> my_lang_db = Languages()
    >>> my_lang_db.load('languages_database')
    >>> guess_the_language(my_lang_db)
'''
from random import choice
from baltoslav.ai import Languages


def guess_the_language(languages: Languages):
    '''
    The offline version of Guess the Language. In this version you have five lives, five suggestions
    and you earn one point per good answer. You need to copy/paste you answer in the input field.

    Parameters
    ----------
    languages : Languages
        The database on which the game will be based.
    '''
    lives = 5
    points = 0
    while lives:
        # Languages selection
        chosen_langs = []
        langs = list(languages.keys())
        while len(chosen_langs) < 5:
            lang = choice(langs)
            if not lang in chosen_langs:
                chosen_langs.append(lang)
        right_lang = chosen_langs[0]

        # Words selection
        chosen_words = []
        words = languages[right_lang]
        while len(chosen_words) < 10:
            word = choice(words)
            if not word in chosen_words:
                chosen_words.append(word)

        print(f'lives.: {lives}')
        print(f'points: {points}')
        print('----- Words')
        print('\n'.join(chosen_words))
        print('----- Languages')
        for _ in range(len(chosen_langs)):
            lang = choice(chosen_langs)
            chosen_langs.remove(lang)
            print(lang)

        summit = input('> ')
        if summit == right_lang:
            points += 1
            print('right answer\n-----\n\n')
        else:
            lives -= 1
            print(f'wrong answer\n{right_lang}\n-----\n\n')
        input()
