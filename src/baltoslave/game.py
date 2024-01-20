from random import choice
import baltoslave.ia as bs


def game():
    languages = bs.Languages()
    languages.load('bs_hybrid')

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
