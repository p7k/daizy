=====
Daizy
=====
| Daizy is an aggregator and player of social network video posts.
| For now it's just a Facebook app DaizyTV_.

.. _DaizyTV: http://apps.facebook.com/daizytv

Dependencies
************
There are a few dependencies with very poor management.  Be careful!

Google AppEngine
----------------
Latest `App Engine SDK for Python`_: version 1.4.0

System level provided.

.. _App Engine SDK for Python: http://code.google.com/appengine/downloads.html

Django Nonrel
-------------
Particularly the `appengine`_ project.

All required libs are symlinked:

- django_
- djangoappengine_
- dbindexer_
- djangotoolbox_

The app itself is actually based on `django testapp`_.

TODO:

- fix unversioned ``django/core/management/commands/runreg.py``
- clean up unnecessary contrib libs and such

.. _appengine: http://www.allbuttonspressed.com/projects/djangoappengine#installation
.. _django: https://bitbucket.org/wkornewald/django-nonrel
.. _djangoappengine: https://bitbucket.org/wkornewald/djangoappengine
.. _dbindexer: https://bitbucket.org/wkornewald/django-dbindexer
.. _djangotoolbox: https://bitbucket.org/wkornewald/djangotoolbox
.. _django testapp: https://bitbucket.org/wkornewald/django-testapp

Django SocialRegistration
-------------------------
Convenience for all things social FB, Twitter, Oauth ...

Symlinked under ``socialregistration``.

Has some of it's own dependencies:

- httplib2
- python-oauth2
- python-openid

All of these are hard copied.

Facebook SDK
------------
Python facebook_sdk_ for Facebook's Graph API.

The SDK module is symlinked into the ``facebook`` app.
``__init__.py`` imports * from SDK + some extensions.
A little hacky.

.. _facebook_sdk: http://github.com/facebook/python-sdk
