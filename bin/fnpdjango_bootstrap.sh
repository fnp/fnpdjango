#!/bin/sh

DJANGO_REQ = 'django>=1.4,<1.5'

mkvirtualenv "$1"
pip install "$DJANGO_REQ"
django-admin.py startproject \
    --template http://pypi.nowoczesnapolska.org.pl/bootstrap/project.tar.gz \
    "$1"
pip install -r "$1"/requirements-dev.txt
