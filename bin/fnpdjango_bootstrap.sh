#!/bin/bash

DJANGO_REQ='django>=1.4,<1.5'
PROJECT="$1"
VIRTUALENVWRAPPER_PATHS="
    /etc/bash_completion.d/virtualenvwrapper
    /usr/bin/virtualenvwrapper.sh
    /usr/local/bin/virtualenvwrapper.sh
"

# Colorful output.
strong='\e[0;32m'
normal='\e[0m'

if [ -z "$PROJECT" ]
then
    echo "Usage:"
    echo "    fnpdjango_bootstrap.sh <project_name>"
    echo "or:"
    echo "    wget <remote_path> -O-|bash /dev/stdin edumedfnpdjango_bootstrap.sh <project_name>"
fi


for venv in $VIRTUALENVWRAPPER_PATHS
do
    if [ -e "$venv" ]
    then
        VIRTUALENVWRAPPER="$venv"
        break
    fi
done
if [ "$VIRTUALENVWRAPPER" ]
then
    echo "virtualenvwrapper found at $VIRTUALENVWRAPPER."
    source "$VIRTUALENVWRAPPER"
else
    echo "ERROR: virtualenvwrapper not found. Tried locations:"
    echo "$VIRTUALENVWRAPPER_PATHS"
    echo "Install virtualenvwrapper or add the correct path to this script."
    echo "Aborting."
    exit
fi

echo -e "${strong}Creating virtualenv: $PROJECT...${normal}"
mkvirtualenv "$PROJECT"
echo -e "${strong}Installing Django...${normal}"
pip install "$DJANGO_REQ"

echo -e "${strong}Starting the project...${normal}"
django-admin.py startproject \
    --template http://pypi.nowoczesnapolska.org.pl/bootstrap/project.tar.gz \
    "$PROJECT"

cd "$PROJECT"
chmod +x manage.py
mv "$1"/localsettings.py.default "$PROJECT"/localsettings.py

echo -e "${strong}Installing requirements...${normal}"
pip install -r requirements.txt
echo -e "${strong}Installing developer requirements...${normal}"
pip install -r requirements-dev.txt
echo -e "${strong}Starting new git repository...${normal}"
git init

