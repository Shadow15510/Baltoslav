'''
A small Python AI that plays to Baltoslav, Guess the Language.

Classes
-------
.. autoclass:: Languages
.. autoclass:: BaltoslavAI

Exemples
--------
Assuming ``ia.py`` was imported as follow ::

    >>> import baltoslav.ia as bs

We can create an instance ::

    >>> database = Languages()       # creates a new database
    >>> my_bs = bs.BaltoslavAI(database)
    >>> my_bs.run_training(10)       # launchs a training session
    >>> database.save('bs_exemple')  # saves the changes
'''
import json
import time
import selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Languages:
    '''
    Implements a database as a dictionnary ``{language name: [words]}``. The basic manipulations on
    dict are still available:

    * ``len`` function
    
    * ``in`` operator
    
    * ``keys`` function
    
    * ``values`` function
    
    * ``items`` function

    Attributes
    ----------
    languages : dict
        The database, under the form of a dict: ``{name: [words]}``.

    Methods
    -------
    .. automethod:: load
    .. automethod:: save
    .. automethod:: add_languages
    .. automethod:: identification
    .. automethod:: feed_database
    '''
    def __init__(self, languages=None):
        '''Constructor method.'''
        if not languages:
            languages = {}
        self.languages = languages

    def __len__(self):
        '''Overloads ``len`` function.'''
        return len(self.languages)

    def __contains__(self, name: str):
        '''Overloads ``in`` operator.'''
        return name in self.languages

    def __getitem__(self, name: str):
        '''
        Allow to get the words from a given language.

        Parameters
        ----------
        name : str
            The name of the language.
        '''
        return self.languages[name]

    def keys(self):
        '''Overloads dict.keys function.'''
        return self.languages.keys()

    def values(self):
        '''Overloads dict.values function.'''
        return self.languages.values()

    def items(self):
        '''Overloads dict.items function.'''
        return self.languages.items()

    def load(self, filename: str='bs_languages'):
        '''
        Loads languages from a file.

        Parameters
        ----------
        filename : str, optionnal
            The name of the file to load.
        '''
        with open(f'{filename}.json', 'r', encoding='utf-8') as file:
            self.languages = json.load(file)

    def save(self, filename: str='bs_languages'):
        '''
        Save languages into a file.

        Parameters
        ----------
        filename : str, optionnal
            The name of the file to save to.
        '''
        with open(f'{filename}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.languages))

    def add_languages(self, languages: dict):
        '''
        Adds new languages and new words to the database.

        Parameters
        ----------
        languages : dict
            The languages to add, must be a dict like: ``{name: [words]}``.
        '''
        for name in languages:
            if name not in self.languages:
                self.languages[name] = []
            self.languages[name] = list({*self.languages[name], *languages[name]})

    def identification(self, unknown_words: tuple):
        '''
        Tries to identify the unknown words given by comparing these words with those in the
        database.

        Parameters
        ----------
        unknown_words : tuple
            The words to identify. It must be an iterable.

        Returns
        -------
        matches : list
            The list of the languages that matched: ``[(name, confidence)]``. The languages are
            sorted by decreasing confidence.
        '''
        matches = []
        for name, words in self.languages.items():
            count = 0
            for unknown_word in unknown_words:
                if unknown_word in words:
                    count += 1

            matches.append((
                    name,
                    count
                ))

        nb_words = len(unknown_words)
        matches = [
                (match[0], int(100 * match[1] / nb_words))
                for match in sorted(matches, key=lambda x: -x[1])
                if match[1]
            ]

        return matches

    def feed_database(self):
        '''Artificially expand the database.'''
        response = requests.get('https://baltoslav.eu/adhadaj/index.php?mova=fr', timeout=10)
        page = BeautifulSoup(response.text, features='html5lib')
        new_languages = {}
        for html_language in page.find_all('span', {'class': 'aaa'}):
            language = list(html_language.parent.parent.strings)
            name, words = language[0], language[2].split()
            new_languages[name] = words
        self.add_languages(new_languages)


class BaltoslavAI:
    '''
    This class implements a small AI that plays Baltoslav.

    Attributes
    ----------
    limit : int
        The maximum number of guess before exiting the game.
    languages : Languages
        The database, under the form of a Languages's instance.
    game_lang : str
        The language code.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: run_training
    .. automethod:: run_playing
    '''
    limit = 500

    def __init__(self, languages: Languages, game_lang: str='en'):
        '''
        Constructor method.

        Parameters
        ----------
        languages : baltoslav.Languages
            The database, under the form of a Languages's instance.
        game_lang : str, optionnal
            The language code.
        '''
        self.languages = languages
        self.game_lang = game_lang

    def __get_button(self, buttons: list, found_languages: list):
        '''
        Finds the best button to click. If the first language found is not one of the available
        buttons, it takes the next language. If identification fails, it will click on a randomly
        chosen button.

        Parameters
        ----------
        buttons : list
            The list of available buttons.

        found_languages : list
            The list of the languages that matched, sorted by decreasing confidence, e.g. the output
            of ``Baltoslav.identification``.

        Returns
        -------
        lang : str
            The language of the clicked button.
        '''
        for lang, _ in found_languages:
            for button in buttons:
                if button.text == lang:
                    button.click()
                    print('.. found')
                    print(f'.. {lang}')
                    return lang

        lang = buttons[0].text
        buttons[0].click()
        print('.. fail')
        print('.. random')
        return lang

    def __main(self, driver: selenium.webdriver, training: bool=True):
        '''
        Trains the AI by playing.

        Parameters
        ----------
        driver : selenium.webdriver
            The web driver.
        training : bool, optionnal
            Specify if the AI should run in training or playing mode:
            * in training mode, the AI memorize the new words;
            * in playing mode, the AI doesn't memorize.

        Returns
        -------
        index : int
            The number of correct guesses plus, possibly, the three permitted errors.
        '''
        index = 0
        while True:
            # Finds and extracts the words from the webpage.
            words = [i.text for i in driver.find_elements(By.CLASS_NAME, 'prawy')]
            index += 1
            if not words:
                return index
            print(f'----- {index}')
            print('words.........:', words)

            # Tries to identify the language.
            print('identification:')
            if index < self.limit:
                found_languages = self.languages.identification(words)
                if found_languages:
                    for lang, confidence in found_languages:
                        print(f'.. {lang} ({confidence}%)')
                else:
                    print('.. fail')
            else:
                found_languages = [('', None)]
                print('.. bypass')

            # Find and click on a button.
            print('button........:')
            lang = self.__get_button(
                    driver.find_elements(By.CLASS_NAME, 'guzik'),
                    found_languages
                )

            # Compares the proposed result with the right one.
            print('results.......:')
            try:
                # If this element exists, then the proposed languages was wrong.
                lang = driver.find_element(By.CLASS_NAME, 'ziel').text
                print('.. fail')
                driver.find_element(By.CLASS_NAME, 'guzik').click()
            except selenium.common.exceptions.NoSuchElementException:
                print('.. sucess')

            # In training mode, adds the words to the database.
            if training and lang:
                self.languages.add_languages({lang: words})

            print('..', lang)
            print()
            time.sleep(0.3)

        return index

    def run_training(self, iterations: int=1):
        '''
        Runs the AI in training mode: create a web driver and launches training.

        Parameters
        ----------
        iterations : int, optionnal
            The number of training sessions.
        '''
        driver = webdriver.Firefox()
        driver.get(f'https://baltoslav.eu/adhadaj/index.php?co=g&mova={self.game_lang}')
        time.sleep(2)
        consent = driver.find_element(By.CLASS_NAME, 'fc-dialog-container')
        button = consent.find_element(By.CLASS_NAME, 'fc-button').click()
        time.sleep(1)
        for i in range(iterations):
            self.__main(driver, training=True)
            if (i + 1) < iterations:
                driver.find_element(By.CLASS_NAME, 'guzik').click()
                print('\n\n')

    def run_playing(self):
        '''Runs the AI in playing mode.'''
        driver = webdriver.Firefox()
        driver.get(f'https://baltoslav.eu/adhadaj/index.php?co=g&mova={self.game_lang}')
        time.sleep(2)
        consent = driver.find_element(By.CLASS_NAME, 'fc-dialog-container')
        button = consent.find_element(By.CLASS_NAME, 'fc-button').click()
        time.sleep(1)
        self.__main(driver, training=False)
