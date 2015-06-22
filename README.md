Sistema de Votação Eletrônica Helios/UNICAMP
===========================================

1. Instalação e configuração do banco de dados PostgreSQL

  * Instalação do servidor: `yum install postgresql-server postgresql-devel python-devel`
  * Inicialização dos diretórios: `service postgresql initdb`
  * Inicialização do serviço: `/etc/init.d/postgresql start`
  * Alterar autenticação no localhost para `md5` ao invés de `ident` em `/var/lib/pgsql/data/pg_hba.conf`
  * Definir a senha para usuário: `passwd postgres` e criar banco de dados: `su - postgres; createdb helios`

2. Instalação e configuração do cliente LDAP:
 * Instalação do pacote: `yum install openldap-devel`
 * Instalação do certificado raiz em `/etc/openldap/certs`
 * Configuração do cliente em `/etc/openldap/ldap.conf`
 ```
#
# LDAP Defaults
#

# See ldap.conf(5) for details
# This file should be world readable but not world writable.

BASE    dc=unicamp,dc=br
URI     ldaps://ldap1.unicamp.br ldaps://ldap2.unicamp.br

#SIZELIMIT      12
#TIMELIMIT      15
#DEREF          never

TLS_CACERTDIR   /etc/openldap/certs
```
 
3. Download dessa versão do Helios: `cd /opt; git clone --recursive; git://github.com/dfaranha/helios-server.git`

4. Instalação do Django via PIP
  * Instalação do PIP: `yum install python-pip python-virtualenv`
  * Criação e utilização do do sandbox: `virtualenv venv; source venv/bin/activate`
  * Instalação da versão 1.4: `cd helios-server; pip install -r requirements.txt`

5. Configuração do Helios no arquivo `settings.py`

 ```
ADMINS = (
     ('Administrator', 'root'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_from_env('SECRET_KEY', '<definir segredo para o Django>')

TIME_ZONE = 'America/Sao_Paulo'

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'HOST': 'localhost',
         'NAME': 'helios',
         'USER': 'postgres',
         'PASSWORD': '<password definido acima>'
     }
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

LANGUAGES = (
    ('en', _('English')),
    ('pt-br', _('Brazilian Portuguese')),
)

MIDDLEWARE_CLASSES = (
    # make all things SSL
    #'sslify.middleware.SSLifyMiddleware',

    # secure a bunch of things
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'

   # 'flatpages_i18n.middleware.FlatpageFallbackMiddleware'
)

TEMPLATE_DIRS = (
    ROOT_PATH,
    os.path.join(ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djangosecure',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    ## needed for queues
    'djcelery',
    'kombu.transport.django',
    ## needed for schema migration
    'south',
    ## HELIOS stuff
    'helios_auth',
    'helios',
    'server_ui',
    'sslserver',
)

# The two hosts are here so the main site can be over plain HTTP
# while the voting URLs are served over SSL.
URL_HOST = get_from_env("URL_HOST", "https://evote.unicamp.br:8080")

# IMPORTANT: you should not change this setting once you've created
# elections, as your elections' cast_url will then be incorrect.
# SECURE_URL_HOST = "https://localhost:8443"
SECURE_URL_HOST = get_from_env("SECURE_URL_HOST", "https://evote.unicamp.br:8080")

# this additional host is used to iframe-isolate the social buttons,
# which usually involve hooking in remote JavaScript, which could be
# a security issue. Plus, if there's a loading issue, it blocks the whole
# page. Not cool.
SOCIALBUTTONS_URL_HOST= get_from_env("SOCIALBUTTONS_URL_HOST", "https://evote.unicamp.br:8080")

AUTH_LDAP_SERVER_URI = 'ldaps://ldap1.unicamp.br' # replace by your ldap URI

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=unicamp,dc=br",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "cn",
}

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_ALWAYS_UPDATE_USER = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)
```

6. Testando o Helios: `python manage.py test`

7. Executando o Helios com visibilidade externa: `python manage.py runsslserver --addrport 0.0.0.0:8080`

8. Habilitar o tratamento de tarefas periódicas: `python manage.py celeryd`

