
import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('MYWEB_ENV', '')

if env:
    if not env.endswith('_settings'):
        env ='{}_settings'.format(env)
    else:
        env = 'settings'

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "myweb.{}".format(env)
)

application = get_wsgi_application()
