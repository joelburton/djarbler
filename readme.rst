Djarbler
========

A simple clone of Warbler, written in vanilla Django.

To use::

    $ ./manage.py migrate
    $ ./manage.py runserver

Then visit http://localhost:8000/.

This uses SQLite, for simplicity in people playing with it. It could
easily use a real database, like PostgreSQL.

This doesn't use any add-on products for Django, but it does use Jinja2
for the templates, rather than the more-typical Django Template Language.
