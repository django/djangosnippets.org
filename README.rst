djangosnippets.org
==================

This code is used to power the snippet sharing site, djangosnippets.org

Database Setup Using Windows
-----------------------------------

Download the latest version of PostgreSQL_. Click on the executable to start the installation setup wizard.

Click ``Next``, keeping all the defaults, ensuring that all components are ticked (including pgAdmin 4). Make a note
of the password you choose for the database superuser (postgres). Select the default port 5432 and the default locale.
After it’s finished installing, you do not need to launch Stack Builder. Un-tick that box if you are asked, and
click ``Finish``.

Open the pgAdmin 4 app. Type in the password you made a note of earlier. The following steps can also be taken using
your windows CLI: Click on ``Servers`` in the Browser pane on the left. Right click on ``PostgreSQL`` and then click
on ``Create``, then ``Database``. In the Database field which you should now see, type 'djangosnippets', then click
``Save``. You should now have two databases in the Browser pane on the left, one being an empty database called
djangosnippets.

Add the below to the bottom of djangosnippets/settings/development.py and djangosnippets/settings/testing.py files::

  DATABASES = {
    'default': {
        'NAME': 'djangosnippets',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
  }

Please do **not** commit the two file changes above. You have now installed and configured your PostgreSQL database
for development.

Development Setup
-----------------

In a Python 3.7 virtual environment::

    $ cd requirements
    $ pip install -r development.txt
    $ cd ..
    $ python manage.py migrate

Now you can start the development server (you may need to set the ALLOWED_HOSTS environment variable first)::

    $ python manage.py runserver

Before you can actually use the site, you have to define at least one
language. If you just want to use the ones from djangosnippets.org, they
are included in the fixtures folder. Also included are five snippets to get you started::

    $ python manage.py createsuperuser
    $ python manage.py loaddata fixtures/cab.json

You will need to build the site.css with tailwindcss::

    $ npm run build

Now you should be able to use the development version of djangosnippets
on port 8000.

To run tests::

    $ python manage.py test --settings=djangosnippets.settings.testing

Docker
------
You need to copy .env.example to .env and configure to your needs. The example is fine to start with development.

You may wish to use docker locally for production dependency testing and development; here are the setup instructions::

    $ docker-compose -f docker-compose.yml build
    $ docker-compose -f docker-compose.yml up -d

-d denotes running docker in a detached state::

    $ docker-compose -f docker-compose.yml run web python manage.py migrate
    $ docker-compose -f docker-compose.yml run web python manage.py createsuperuser
    $ docker-compose -f docker-compose.yml run web python manage.py loaddata fixtures/cab.json
    $ npm run build
    $ docker-compose -f docker-compose.yml run web python manage.py collectstatic


The docker setup is running as close as possible to the production setup in Heroku:

Postgres 12.3
Gunicorn
Redis

To run our tests with docker::

    $ docker-compose -f docker-compose.yml run web python manage.py test --settings=djangosnippets.settings.testing

Styling Contributor?
--------------------

DjangoSnippets uses the Foundation_ framework as the core of its visual style. To
get this working on your local machine you need compass_ and bower_ to compile
your stylesheets. Please **never** modify the generated .css files directly. Use the .scss ones instead.

To keep the setup path as short as possible, run the following commands
in your terminal::

    $ cd djangosnippets/static
    $ bower install && compass watch

If you don't have either of these two installed, you can find detailed
instructions on their respective websites.

Please make sure that you commit only a compressed version of the CSS file
as this is what will be deployed. (In order to do that the default
configuration inside `djangosnippets/static/config.rb` is
`output_style = :compressed`)


Production Setup
----------------

The production setup is currently tailored to Heroku and, therefore, mostly
automatic. The difference between these two setups is configured in
the djangosnippets.settings.production module and the requirements.txt file.

.. _bower: http://bower.io/
.. _compass: http://compass-style.org/install/
.. _foundation: http://foundation.zurb.com/
.. _PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

