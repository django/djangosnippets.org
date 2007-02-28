===
Cab
===

Cab (named for the jazz bandleader and scat singer Cab Calloway) is a
Django application which allows users to post and share useful
"snippets" of code.


Installation notes
==================

Cab has a couple of external dependencies:

    * `Pygments`_ for code highlighting.

    * `python-markdown`_ for processing snippet descriptions. Other
      Python ports of Markdown will not work, since the code which
      calls Markdown assumes the existence of python-markdown's "safe
      mode".

Additionally, the default setup requires a few applications which are
bundled with Django itself:

    * ``django.contrib.comments`` to enable commenting.

    * ``django.contrib.markup`` to handle Markdown formatting of
       comments.

    * ``django.contrib.syndication`` to enable feeds.

It's also recommended that you have ``django.contrib.admin`` installed
for ease of site maintenance.

Once you've got those taken care of, do a Subversion checkout of Cab
from somewhere on your Python path::

    svn checkout http://cab.googlecode.com/svn/trunk/ cab

Then add ``cab`` to the ``INSTALLED_APPS`` setting of your Django
project, run ``manage.py syncdb``, and either put a call to
``include('cab.urls')`` somewhere in your root URLConf or copy over
the URL patterns from Cab that you want to use.

.. _Pygments: http://pygments.org/
.. _python-markdown: http://www.freewisdom.org/projects/python-markdown/


Templates
=========

The Subversion checkout will get you a set of example templates
matching those currently in use on `djangosnippets.org`_, but they
assume the existence of base project-wide templates used by that site;
you'll need to either create templates with the same names to extend,
or edit the included templates to suit your site's layout.

If you choose to simply create the appropriate base templates, you
shouldn't need to do anything special to pick them up; Django's "app
directories" template loader should notice them and use them.

.. _djangosnippets.org: http://www.djangosnippets.org/