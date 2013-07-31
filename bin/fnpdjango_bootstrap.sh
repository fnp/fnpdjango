#!/bin/bash
#
# Use as: 
#
#   source <(curl -L pypi.nowoczesnapolska.org.pl/django)
#


PROJECT="$1"

# Make it a function, so that it works with `source`
start_project() {

DJANGO_REQ='Django>=1.5,<1.6'
DJANGO_ROOT='src'
PROJECT_TEMPLATE='http://git.nowoczesnapolska.org.pl/?p=fnpdjango.git;a=snapshot;h=64c636d1e3ff35a7a1d3394fd1d3ff0093f44aa2;sf=tgz'
VIRTUALENVWRAPPER_PATHS="
    /etc/bash_completion.d/virtualenvwrapper
    /usr/bin/virtualenvwrapper.sh
    /usr/local/bin/virtualenvwrapper.sh
"

# Colorful output.
strong='\e[0;32m'
error='\e[1;31m'
normal='\e[0m'

echo "Create new Django project."
while [ -z "$PROJECT" ]
do
    echo "Name of the project:"
    read PROJECT
done
echo -e "Project: ${strong}${PROJECT}${normal}"

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
    echo -e "${error}ERROR: virtualenvwrapper not found. Tried locations:${normal}"
    echo "$VIRTUALENVWRAPPER_PATHS"
    echo -e "${error}Install virtualenvwrapper or add the correct path to this script.${normal}"
    echo "Aborting."
    return
fi

echo -e "${strong}Creating virtualenv: $PROJECT...${normal}"
mkvirtualenv "$PROJECT"
echo -e "${strong}Installing Django...${normal}"
pip install "$DJANGO_REQ"

echo -e "${strong}Starting the project...${normal}"
django-admin.py startproject \
    --template "$PROJECT_TEMPLATE" \
    "$PROJECT"

cd "$PROJECT"

WRAPPER="`ls`"
mv "$WRAPPER/"* "$WRAPPER/".gitignore .
rmdir "$WRAPPER"

chmod +x "$DJANGO_ROOT"/manage.py
mv "$DJANGO_ROOT/$PROJECT/localsettings.py.dev" "$DJANGO_ROOT/$PROJECT/localsettings.py"

echo -e "${strong}Installing requirements...${normal}"
pip install -r requirements.txt
echo -e "${strong}Installing developer requirements...${normal}"
pip install -r requirements-dev.txt
echo -e "${strong}Running syncdb...${normal}"
"$DJANGO_ROOT"/manage.py syncdb --noinput

echo -e "${strong}Starting new git repository...${normal}"
git init

echo -e "${strong}What next?${normal}"
echo " * Work on your app, commit to git."
echo " * Review fabfile, use fab for deployment."


}
start_project
