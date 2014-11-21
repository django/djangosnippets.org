djangosnippets.org
==================

This code is used to power the snippet sharing site, djangosnippets.org


Development setup
-----------------

::
    
    $ cd requirements
    $ pip install -r development.txt
    $ cd ..
    $ python manage.py syncdb --migrate

Now you can start the develoment server::
    
    $ python manage.py runserver

Before you can actually use the site now you have to define at least one
language. If you just want to use the ones from djangosnippets.org, they
are included in the fixtures folder::
    
    $ python manage.py loaddata fixtures/languages.json

Now you should be able to use the development version of djangosnippets
on port 8000.


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
