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

"""
from fabric.api import *
from os.path import abspath, dirname, exists, join
from fabric.contrib import files
from fabric.tasks import Task, execute

env.virtualenv = '/usr/bin/virtualenv'
env.services = None


@task
def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories.
    virtualenv should be already installed.
    """
    require('hosts', 'app_path', 'virtualenv')

    run('mkdir -p %(app_path)s' % env, pty=True)
    run('%(virtualenv)s %(app_path)s/ve' % env, pty=True)
    run('mkdir -p %(app_path)s/releases %(app_path)s/packages' % env, pty=True)
    run('cd %(app_path)s/releases; ln -sfT . current; ln -sfT . previous' % env, pty=True)
    upload_samples()
    print "Fill out db details in localsettings.py and run deploy."


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

    check_setup()
    upload_tar_from_git()
    install_requirements()
    copy_localsettings()
    symlink_current_release()
    migrate()
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
class DebianGunicorn(Task):
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name

    def run(self):
        print '>>> restart webserver using gunicorn-debian'
        with path('/sbin'):
            sudo('gunicorn-debian restart %s' % self.site_name, shell=False)

class Apache(Task):
    def run(self):
        print '>>> restart webserver by touching WSGI'
        with path('/sbin'):
            run('touch %(app_path)s/%(project_name)s/wsgi.py' % env)

class Supervisord(Task):
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name

    def run(self):
        print '>>> supervisord: restart %s' % self.name
        with path('/sbin'):
            sudo('supervisorctl restart %s' % self.name, shell=False)

def check_setup():
    require('app_path')
    try:
        run('[ -e %(app_path)s/ve ]' % env)
    except SystemExit:
        print "Environment isn't ready. Run `fab setup` first."
        raise

def upload_samples():
    upload_localsettings_sample()
    upload_nginx_sample()
    upload_gunicorn_sample()

def upload_localsettings_sample():
    "Fill out localsettings template and upload as a sample."
    print '>>> upload localsettings template'
    require('app_path', 'project_name')
    template = '%(project_name)s/localsettings.py.template'
    if not exists(template):
        template = join(dirname(abspath(__file__)), 'templates/localsettings.py.template')
    env.secret_key = '' # sth random
    files.upload_template(template, '%(app_path)s/localsettings.py.sample' % env, env)

def upload_nginx_sample():
    "Fill out nginx conf template and upload as a sample."
    print '>>> upload nginx template'
    require('app_path', 'project_name')
    template = '%(project_name)s/nginx.template'
    if not exists(template):
        template = join(dirname(abspath(__file__)), 'templates/nginx.template')
    files.upload_template(template, '%(app_path)s/nginx.sample' % env, env)

def upload_gunicorn_sample():
    "Fill out gunicorn conf template and upload as a sample."
    print '>>> upload gunicorn template'
    require('app_path', 'project_name')
    template = '%(project_name)s/gunicorn.template'
    if not exists(template):
        template = join(dirname(abspath(__file__)), 'templates/gunicorn.template')
    files.upload_template(template, '%(app_path)s/gunicorn.sample' % env, env)

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
    run('cd %(app_path)s; ve/bin/pip install -r %(app_path)s/releases/%(release)s/requirements.txt' % env, pty=True)

def copy_localsettings():
    "Copy localsettings.py from root directory to release directory (if this file exists)"
    print ">>> copy localsettings"
    require('release', provided_by=[deploy])
    require('app_path', 'project_name')

    with settings(warn_only=True):
        run('cp %(app_path)s/localsettings.py %(app_path)s/releases/%(release)s/%(project_name)s' % env)

def symlink_current_release():
    "Symlink our current release"
    print '>>> symlink current release'
    require('release', provided_by=[deploy])
    require('app_path')
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous')
        run('ln -s %(release)s releases/current' % env)

def migrate():
    "Update the database"
    print '>>> migrate'
    require('app_path', 'project_name')
    with cd('%(app_path)s/releases/current/%(project_name)s' % env):
        run('%(app_path)s/ve/bin/python manage.py syncdb --noinput' % env, pty=True)
        run('%(app_path)s/ve/bin/python manage.py migrate' % env, pty=True)

def collectstatic():
    """Collect static files"""
    print '>>> collectstatic'
    require('app_path', 'project_name')
    with cd('%(app_path)s/releases/current/%(project_name)s' % env):
        run('%(app_path)s/ve/bin/python manage.py collectstatic --noinput' % env, pty=True)
