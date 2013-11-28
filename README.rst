djangosnippets.org
==================

This code is used to power the snippet sharing site, djangosnippets.org


Development setup
-----------------

::

    $ pip install -r requirmenets-dev.txt
    $ python manage.py syncdb --migrate

Now you can start the develoment server::
    
    $ python manage.py runserver

Before you can actually use the site now you have to define at least one
language. If you just want to use the ones from djangosnippets.org, they
are included in the fixtures folder::
    
    $ python manage.py loaddata fixtures/languages.json

Now you should be able to use the development version of djangosnippets
on port 8000.


Production setup
----------------

The production setup is right now tailored to Heroku and therefor mostly
automatic. The difference between these two setups is configured in
the djangosnippets.settings.production module and the requirements.txt.
