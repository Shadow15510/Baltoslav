Tutorial
========

Installation
------------
A PyPI package is available, so you just need to enter ``pip install baltoslav`` into a terminal to install the package.

Creation of a new database
--------------------------
To work, ``baltoslav`` need a languages database, it's a large json file which contains all the known languages and words from the game 'Guess the Language'. You should make a directory to have your database properly stocked::

    $ mkdir bs_project
    $ cd bs_project

Once you're in, you can start in a Python Shell::
    
    >>> import baltoslav.ai as bsai

The first thing to do is to create a ``Languages`` instance::
    
    >>> lang_db = bsai.Languages()

.. note::
    If you already have a database, you can import it by using::
        
        >>> lang_db.load('lang_db')

Here we have two possibilities:

* feed the database by playing to the game;

* force the expansion of the database by gathering words.

Once you've finished with your database, don't forget to save your changes::
    
    >>> lang_db.save('lang_db')

A file ``lang_db.json`` should have appeared in your working directory.

Training mode
-------------
To feed the database by playing, you need to make an instance of ``BaltoslavAI``::

    >>> my_ai = bsai.BaltoslavAI(lang_db)

Then you can run the AI::
    
    >>> my_ai.run_training(10)

Here, the AI will play 10 games before leaving. The more you play, the better the AI will become. Once you've finished, save the database::

    >>> lang_db.save('lang_db')

Forced expansion of the database
--------------------------------
Feeding the database by playing is unefficient because you should play hundreds of games before the AI start to be good, so you can expand the database by adding languages and words in it.

To do that, you just need to enter::
    
    >>> lang_db.feed_database()

You can call this method into a `for` loop to sky rocket your database's size.

Once you've finished, don't forget to save your changes::

    >>> lang_db.save('lang_db')

Playing mode
------------
When your database is big enough, you can launch your AI, but without training i.e. it won't remember the words and won't progress. This mode can be useful to see how many points the AI can make.

To launch the AI in playing mode::

    >>> my_ai.run_playing()

Offline 'Guess the Language'
----------------------------
This package also provide an offline copy of 'Guess the Language'. To play you need a database, the biggest, the better.

To play, you have to import the package ``game``::

    >>> import baltoslav.game as bsg
    >>> from baltoslav.ai import Languages
    >>> lang_db = Languages()
    >>> lang_db.load('lang_db')
    >>> bsg.guess_the_language(lang_db)

No need to save the database, this function is read-only. In this version of the game, you have 5 lives (against 3 in the real game), 1 point per good answer and 5 suggested languages. You need to write the right language in the input field.

Minimal Working Exemple
-----------------------
A small overview of all that have been said here::

    >>> import baltoslav.ai as bsai
    >>> lang_db = bsai.Languages()  # creation of a database
    >>> land_db.load('lang_db')     # loading an existing database
    >>> ai = bsai.BaltoslavAI(lang_db)  # creation of an AI
    >>> ai.run_training(10)      # train the AI on 10 games
    >>> lang_db.save('lang_db')  # save the new languages and words learned
