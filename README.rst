djangosnippets.org
==================

This code is used to power the snippet sharing site, djangosnippets.org


Development setup
-----------------

In a Python 3.7 virtual environment::

    $ cd requirements
    $ pip install -r development.txt
    $ cd ..
    $ python manage.py migrate

Now you can start the development server::

    $ python manage.py runserver

Before you can actually use the site now you have to define at least one
language. If you just want to use the ones from djangosnippets.org, they
are included in the fixtures folder. Also included are 5 snippets to get you started::

    $ python manage.py loaddata fixtures/cab.json

Now you should be able to use the development version of djangosnippets
on port 8000.

Docker 
------

You may wish to use docker locally for production dependency testing and development, here are the setup instructions::

    $ docker-compose -f docker-compose.yml build
    $ docker-compose -f docker-compose.yml up -d 

-d denotes running docker in a detached state::

    $ docker-compose -f docker-compose.yml run web python manage.py migrate
    $ docker-compose -f docker-compose.yml run web python manage.py loaddata fixtures/cab.json
    $ docker-compose -f docker-compose.yml run web python manage.py createsuperuser
    $ docker-compose -f docker-compose.yml run web python manage.py collectstatic

The docker setup is running as close as possible to the production setup in heroku:

Postgres 12.3
Gunicorn
Redis

To run our tests with docker run the following:

    $ docker-compose -f docker-compose.yml run web python manage.py test --settings=cab.tests.settings

Styling contributor?
--------------------

DjangoSnippets uses the Foundation_ framework as core of its visual style. To
get this working on your local machine you need compass_ and bower_ to compile
your stylesheets. Please **never** modify the generated .css files directly
but use the .scss ones.

To keep the setup path as short as possible, simply run following commands
in your terminal::

    $ cd djangosnippets/static
    $ bower install && compass watch

If you don't have either of these two installed, you can find detailed
instructions on their respective websites.

Please make sure, that you commit only a compressed version of the CSS file
as this is what will be deployed.


Production setup
----------------

The production setup is right now tailored to Heroku and therefore mostly
automatic. The difference between these two setups is configured in
the djangosnippets.settings.production module and the requirements.txt.

.. _bower: http://bower.io/
.. _compass: http://compass-style.org/install/
.. _foundation: http://foundation.zurb.com/


