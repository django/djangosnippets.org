===
Cab
===

Cab (named for the jazz bandleader and scat singer Cab Calloway) is a
Django application which allows users to post and share useful
"snippets" of code.

This code is used to power the snippet sharing site, djangosnippets.org

Installation notes
==================

Cab has a couple of external dependencies:

* `Pygments`_ for code highlighting.

* `python-markdown`_ for processing snippet descriptions. Other
  Python ports of Markdown will not work, since the code which
  calls Markdown assumes the existence of python-markdown's "safe
  mode".

* `django-simple-ratings`_ for item ranking

* `django-taggit`_ for tagging

* ``django_comments`` to enable commenting.

Additionally, the default setup requires a few applications which are
bundled with Django itself:

* ``django.contrib.syndication`` to enable feeds.

It's also recommended that you have ``django.contrib.admin`` installed
for ease of site maintenance.

Add ``ratings``, ``taggit`` and ``cab`` to the ``INSTALLED_APPS`` setting
of your Django project, run ``manage.py syncdb``, and either put a call to
``include('cab.urls.snippets')`` somewhere inn your root URLConf or copy over
the URL patterns from Cab that you want to use.

Note that the ``get_absolute_url`` methods of the ``Language``,
``Snippet`` and ``Tag`` models assume that they will live under the
URLs ``/languages/``, ``/snippets/`` and ``/tags/``, so if you want
them to go elsewhere you'll need to edit those methods or ovveride
them with Django's ``ABSOLUTE_URL_OVERRIDES`` setting.

.. _Pygments: http://pygments.org/
.. _python-markdown: http://www.freewisdom.org/projects/python-markdown/
.. _django-simple-ratings: http://github.com/coleifer/django-simple-ratings/
.. _django-taggit: http://github.com/alex/django-taggit/


Templates
=========

The git repo will get you a set of example templates
matching those currently in use on `djangosnippets.org`_
