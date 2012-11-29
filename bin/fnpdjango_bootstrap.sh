#!/bin/sh

DJANGO_REQ = 'django>=1.4,<1.5'

mkvirtualenv "$1"
pip install "$DJANGO_REQ"
django-admin.py startproject \
    --template http://pypi.nowoczesnapolska.org.pl/bootstrap/project.tar.gz \
    "$1"

cd "$1"
chmod +x manage.py
mv "$1"/localsettings.py.default "$1"/localsettings.py
pip install -r requirements.txt
pip install -r requirements-dev.txt
git init

