from fnpdjango.deploy import *

env.project_name = '{{ project_name }}'
env.hosts = ['giewont.icm.edu.pl']
env.user = '{{ project_name }}'
env.app_path = '/srv/{{ project_name }}'
env.services = [
    DebianGunicorn('{{ project_name }}'),
]
env.django_root_path = 'src'

