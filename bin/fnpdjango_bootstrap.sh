#!/bin/bash
#
# Use as: 
#
#   source <(curl d.nowoczesnapolska.org.pl)
#


PROJECT="$1"

# Make it a function, so that it works with `source`
start_project() {

DJANGO_REQ='Django>=1.6,<1.7'
DJANGO_ROOT='src'

PYPI='http://pypi.nowoczesnapolska.org.pl/simple'
PROJECT_TEMPLATE='http://git.nowoczesnapolska.org.pl/?p=fnpdjango.git;a=snapshot;h=project;sf=tgz'

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
pip install -i "$PYPI" "$DJANGO_REQ"
pip install -i "$PYPI" --pre django-startproject-plus

echo -e "${strong}Starting the project...${normal}"
django-startproject.py \
    --template "$PROJECT_TEMPLATE" \
    --name NOTICE \
    --extra_context='{"year": "`date +%Y`"}' \
    "$PROJECT"

cd "$PROJECT"

# GitWeb adds a top directory to the snapshot, let's remove it.
if [ ! -e .gitignore ]
then
    WRAPPER="`ls`"
    mv "$WRAPPER/"* "$WRAPPER/".gitignore .
    rmdir "$WRAPPER"
fi

chmod +x "$DJANGO_ROOT"/manage.py
mv "$DJANGO_ROOT/$PROJECT/localsettings.py.dev" "$DJANGO_ROOT/$PROJECT/localsettings.py"

echo -e "${strong}Installing requirements...${normal}"
pip install -i "$PYPI" -r requirements.txt
echo -e "${strong}Installing developer requirements...${normal}"
pip install -i "$PYPI" -r requirements-dev.txt
echo -e "${strong}Running syncdb...${normal}"
"$DJANGO_ROOT"/manage.py syncdb --noinput

echo -e "${strong}Starting new git repository...${normal}"
git init

echo -e "${strong}What next?${normal}"
echo " * Work on your app, commit to git."
echo " * Review fabfile, use fab for deployment."


}
start_project

# The following is just for displaying it as a webpage:<!--
#--><style>body{white-space:pre;color:#ddd}</style><h1 style="color:#000;text-align:center;position:fixed;top:0;bottom:0;left:0;right:0;white-space:normal">source &lt;(curl <span id="location"></span>)</h1><script>document.getElementById('location').innerHTML=window.location;</script>

