djangosnippets.org
==================

This code is used to power the snippet sharing site, `djangosnippets.org`_

Development Setup
=================

Prerequisites
-------------

- Python version 3.11
- PostgreSQL
- `uv`_ - An extremely fast Python package and project manager

Installation
------------

Basic Installation
~~~~~~~~~~~~~~~~~~

1. Clone the repo:

   .. code-block:: console

      https://github.com/django/djangosnippets.org.git

2. Install uv if you haven't already:

   .. code-block:: console

      # macOS
      curl -LsSf https://astral.sh/uv/install.sh | sh
      # Windows
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

3. Connect to PostgreSQL

   Connect in Linux:

   .. code-block:: console

      psql -U $(whoami) -d postgres

   Connect in Windows:

   .. code-block:: console

      psql -U postgres

4. Create a PostgreSQL database and role:

   .. code-block:: console

      postgres=# CREATE DATABASE djangosnippets;
      postgres=# CREATE USER djangosnippets WITH SUPERUSER PASSWORD 'djangosnippets';
      postgres=# GRANT ALL PRIVILEGES ON DATABASE djangosnippets TO djangosnippets;

   Exit psql shell:

   .. code-block:: console

      postgres=# exit

5. Install dependencies:

   .. code-block:: console

      uv sync --extra dev

6. Copy `.env.template.local` file, rename to `.env` and configure variables for your local postgres database.

   Copy in Linux:

   .. code-block:: console

      cp .env.template.local .env

   Copy in Windows:

   .. code-block:: console

      copy .env.template.local .env

7. Run migrations and create superuser:

   Migrate:

   .. code-block:: console

      uv run python manage.py migrate

   Create superuser:

   .. code-block:: console

      uv run python manage.py createsuperuser

   Optionally load data:

   .. code-block:: console

      uv run python manage.py loaddata fixtures/cab.json

8. Install tailwind (npm is required):

   .. code-block:: console

      uv run python manage.py tailwind install

9. Run server locally:

   .. code-block:: console

      uv run python manage.py runserver_plus

10. Run tailwind in another terminal locally:

    .. code-block:: console

      uv run python manage.py tailwind start

With Docker
~~~~~~~~~~~~~~~~~~~

Using `Docker <https://www.docker.com/products/docker-desktop/>`_ allows you to set up the development environment more quickly if Docker is installed 🐳

1. Build the Docker images:

   .. code-block:: console

      docker compose -f docker-compose.local.yml build

2. Start the containers:

   .. code-block:: console

      docker compose -f docker-compose.local.yml up -d

3. Go to: http://127.0.0.1:8000/ and enjoy 🙌

Docker
======
You need to copy .env.example to .env and configure to your needs. The example is fine to start with development.

You may wish to use docker locally for production dependency testing and development; here are the setup instructions::

    $ docker-compose -f docker-compose.production.yml build
    $ docker-compose -f docker-compose.production.yml up -d

-d denotes running docker in a detached state::

    $ docker-compose -f docker-compose.production.yml run web python manage.py migrate
    $ docker-compose -f docker-compose.production.yml run web python manage.py createsuperuser
    $ docker-compose -f docker-compose.production.yml run web python manage.py loaddata fixtures/cab.json
    $ npm run build
    $ docker-compose -f docker-compose.production.yml run web python manage.py collectstatic


The docker setup is running as close as possible to the production setup in Heroku:

Postgres 12.3
Gunicorn
Redis

To run our tests with docker::

    $ docker-compose -f docker-compose.yml run web python manage.py test --settings=djangosnippets.settings.testing

Test
======
To run tests::

    $ python manage.py test --settings=djangosnippets.settings.testing

Styling Contributor?
====================

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
================

The production setup is currently tailored to Heroku and, therefore, mostly
automatic. The difference between these two setups is configured in
the `djangosnippets.settings.production <./djangosnippets/settings/production.py>`_ module and the `requirements.txt <./requirements.txt>`_ file.

.. _bower: http://bower.io/
.. _compass: http://rubygems.org/gems/compass/
.. _foundation: http://foundation.zurb.com/
.. _djangosnippets.org: https://djangosnippets.org/
.. _uv: https://docs.astral.sh/uv/
.. _document: https://docs.astral.sh/uv/getting-started/installation/
.. _PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
