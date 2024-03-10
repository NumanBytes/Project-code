from .base import *

connect_to_db_on_render=env.bool('DEPLOY_ON_RENDER', False)
if not connect_to_db_on_render:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str('POSTGRES_DB','lootlo_db'),
            'USER': env.str('POSTGRES_USER','lootlo'),
            'PASSWORD': env.str('POSTGRES_PASSWORD','lootlo'),
            'HOST': env.str('DB_HOST','localhost'),
            'PORT': env.str('DB_PORT',''),
        }
    }
else:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(env.str('RENDER_DB_URL','*******'))}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')
