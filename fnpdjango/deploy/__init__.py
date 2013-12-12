"""
Generic fabric deployment script.
Create a fabfile.py in the project and start it with:

    from fnpdjango.deploy import *

Then set up some env properties:
    project_name: slug-like project name
    hosts: list of target host names
    user: remote user name
    app_path: where does the app go
    services: list of tasks to run after deployment
    django_root_path (optional): path to the directory
        containing django project, relative to the
        root of the repository (defaults to '.')
    localsettings_dst_path (optional): path indicating
        where to copy the localsettings file, relative
        to django_root_path (defaults to project_name/localsettings.py)
    skip_collect_static (optional): if True, Django collectstatic command is not called
"""
from os.path import abspath, dirname, exists, join
from django.utils.crypto import get_random_string
from fabric.api import *
from fabric.contrib import files
from fabric.tasks import Task, execute

env.virtualenv = '/usr/bin/virtualenv'
env.services = None


@task
def setup():
    """
    Setup all needed directories.
    """
    require('hosts', 'app_path')

    if not files.exists(env.app_path):
        run('mkdir -p %(app_path)s' % env, pty=True)
    with cd(env.app_path):
        for subdir in 'releases', 'packages', 'log', 'samples':
            if not files.exists(subdir):
                run('mkdir -p %s' % subdir, pty=True)
    with cd('%(app_path)s/releases' % env):
        if not files.exists('current'):
            run('ln -sfT . current', pty=True)
        if not files.exists('previous'):
            run('ln -sfT . previous', pty=True)
    
    upload_samples()


def check_localsettings():
    if not files.exists('%(app_path)s/localsettings.py' % env):
        abort('localsettings.py file missing.')


@task(default=True)
def deploy():
    """
    Deploy the latest version of the site to the servers,
    install any required third party modules,
    install the virtual host and then restart the webserver
    """
    require('hosts', 'app_path')

    import time
    env.release = time.strftime('%Y-%m-%dT%H%M')

    setup()
    check_localsettings()
    upload_tar_from_git()
    copy_localsettings()
    install_requirements()
    symlink_current_release()
    migrate()
    pre_collectstatic()
    collectstatic()
    restart()

@task
def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    Warning: this will almost certainly go wrong, it there were any migrations
    in the meantime!
    """
    require('hosts', 'app_path')
    with cd(env.path):
        run('mv releases/current releases/_previous;', pty=True)
        run('mv releases/previous releases/current;', pty=True)
        run('mv releases/_previous releases/previous;', pty=True)
    collectstatic()
    restart()

@task
def deploy_version(version):
    """
    Loads the specified version.
    Warning: this will almost certainly go wrong, it there were any migrations
    in the meantime!
    """
    "Specify a specific version to be made live"
    require('hosts', 'app_path')
    env.version = version
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous;', pty=True)
        run('ln -s %(version)s releases/current' % env, pty=True)
    collectstatic()
    restart()

@task
def restart():
    require('services')
    for service in env.services:
        execute(service)


# =====================================================================
# = Helpers. These are called by other functions rather than directly =
# =====================================================================

class Service(Task):
    def upload_sample(self):
        pass

class DebianGunicorn(Service):
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name

    def run(self):
        print '>>> restart webserver using gunicorn-debian'
        sudo('gunicorn-debian restart %s' % self.name, shell=False)

    def upload_sample(self):
        upload_sample('gunicorn')

class Apache(Service):
    def run(self):
        print '>>> restart webserver by touching WSGI'
        with path('/sbin'):
            run('touch %(app_path)s/%(project_name)s/wsgi.py' % env)

class Supervisord(Service):
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name

    def run(self):
        print '>>> supervisord: restart %s' % self.name
        sudo('supervisorctl restart %s' % self.name, shell=False)

class Command(Task):
    def __init__(self, commands, working_dir):
        if not hasattr(commands, '__iter__'):
            commands = [commands]
        self.name = 'Command: %s @ %s' % (commands, working_dir)
        self.commands = commands
        self.working_dir = working_dir

    def run(self):
        require('app_path')
        with cd(join('%(app_path)s/releases/current' % env, self.working_dir)):
            for command in self.commands:
                run(command)

def upload_samples():
    upload_localsettings_sample()
    upload_nginx_sample()
    for service in env.services:
        service.upload_sample()

def upload_sample(name):
    require('app_path', 'project_name')
    upload_path = '%(app_path)s/samples/' % env + name + '.sample'
    if files.exists(upload_path):
        return
    print '>>> upload %s template' % name
    template = '%(project_name)s/' % env + name + '.template'
    if not exists(template):
        template = join(dirname(abspath(__file__)), 'templates/' + name + '.template')
    files.upload_template(template, upload_path, env)

def upload_localsettings_sample():
    "Fill out localsettings template and upload as a sample."
    env.secret_key = get_random_string(50)
    upload_sample('localsettings.py')

upload_nginx_sample = lambda: upload_sample('nginx')

def upload_tar_from_git():
    "Create an archive from the current Git branch and upload it"
    print '>>> upload tar from git'
    require('release', provided_by=[deploy])
    require('app_path')
    local('git-archive-all.sh --format tar %(release)s.tar' % env)
    local('gzip %(release)s.tar' % env)
    run('mkdir -p %(app_path)s/releases/%(release)s' % env, pty=True)
    run('mkdir -p %(app_path)s/packages' % env, pty=True)
    put('%(release)s.tar.gz' % env, '%(app_path)s/packages/' % env)
    run('cd %(app_path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)

def install_requirements():
    "Install the required packages from the requirements file using pip"
    print '>>> install requirements'
    require('release', provided_by=[deploy])
    require('app_path')
    if not files.exists('%(app_path)s/ve' % env):
        require('virtualenv')
        run('%(virtualenv)s %(app_path)s/ve' % env, pty=True)
    with cd('%(app_path)s/releases/%(release)s' % env):
        run('%(app_path)s/ve/bin/pip install -r requirements.txt' % env, pty=True)
    with cd(get_django_root_path(env['release'])):
        # Install DB requirement
        database_reqs = {
            'django.db.backends.postgresql_psycopg2': 'psycopg2',
            'django.db.backends.mysql': 'MySQL-python',
        }
        databases = run('''DJANGO_SETTINGS_MODULE=%(project_name)s.settings %(app_path)s/ve/bin/python -c 'from django.conf import settings;              print " ".join(set([d["ENGINE"] for d in settings.DATABASES.values()]))' ''' % env)
        for database in databases.split():
            if database in database_reqs:
                # TODO: set pip default pypi
                run('%(app_path)s/ve/bin/pip install ' % env + database_reqs[database])


def copy_localsettings():
    "Copy localsettings.py from root directory to release directory (if this file exists)"
    print ">>> copy localsettings"
    require('release', provided_by=[deploy])
    require('app_path', 'project_name')

    with settings(warn_only=True):
        copy_to = join(get_django_root_path(env['release']), env.get('localsettings_dst_path', env['project_name']))
        run('cp %(app_path)s/localsettings.py ' % env + copy_to)

def symlink_current_release():
    "Symlink our current release"
    print '>>> symlink current release'
    require('release', provided_by=[deploy])
    require('app_path')
    with cd(env.app_path):
        run('rm releases/previous; mv releases/current releases/previous')
        run('ln -s %(release)s releases/current' % env)

def migrate():
    "Update the database"
    print '>>> migrate'
    require('app_path', 'project_name')
    with cd(get_django_root_path('current')):
        run('%(app_path)s/ve/bin/python manage.py syncdb --noinput' % env, pty=True)
        run('%(app_path)s/ve/bin/python manage.py migrate' % env, pty=True)

def pre_collectstatic():
    print '>>> pre_collectstatic'
    for task in env.get('pre_collectstatic', []):
        execute(task)

def collectstatic():
    """Collect static files"""
    print '>>> collectstatic'
    if env.get('skip_collect_static', False):
        print '... skipped'
        return
    require('app_path', 'project_name')
    with cd(get_django_root_path('current')):
        run('%(app_path)s/ve/bin/python manage.py collectstatic --noinput' % env, pty=True)


def get_django_root_path(release):
    require('app_path')
    path = '%(app_path)s/releases/%(release)s' % dict(app_path = env['app_path'], release = release)
    if 'django_root_path' in env:
        path = join(path, env['django_root_path'])
    return path