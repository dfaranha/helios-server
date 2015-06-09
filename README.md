Sistema de Votação Eletrônica Helios/UNICAMP
===========================================

1. Instalação e configuração do banco de dados PostgreSQL

  * Instalação do servidor: `yum install postgresql-server postgresql-devel`
  * Inicialização dos diretórios: `service postgresql initdb`
  * Inicialização do serviço: `/etc/init.d/postgresql start`
  * Alterar autenticação no localhost para `md5` ao invés de `ident` em `/var/lib/pgsql/data/pg_hba.conf`
  * Definir a senha para usuário: `passwd postgres` e criar banco de dados com comando
     su - postgres
     <usar a senha definida acima>
     createdb helios

 openldap-devel
 
2. Download dessa versão do Helios: `cd /opt; git clone --recursive; git://github.com/dfaranha/helios-server.git`

3. Instalação do Django via PIP
  * Instalação do PIP: `yum install python-pip python-virtualenv`
  * Criação e utilização do do sandbox: `virtualenv venv; source venv/bin/activate`
  * Instalação da versão 1.4: `cd helios-server; pip install -r requirements.txt`

4. Configuração do Helios no arquivo setting.py

```
TIME_ZONE = 'America/Sao_Paulo'
ADMINS = (
     ('Administrator', 'root'),
)
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'HOST': 'localhost',
         'NAME': 'helios',
         'USER': 'postgres',
         'PASSWORD': '<password definido acima>'
     }
}
LANGUAGE_CODE = 'en-us'
DEFAULT_FROM_EMAIL = get_from_env('DEFAULT_FROM_EMAIL', '<meu email>')
DEFAULT_FROM_NAME = get_from_env('DEFAULT_FROM_NAME', '<teste Helios>')
URL_HOST = get_from_env("URL_HOST", "http://localhost:8080").rstrip("/")


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

5 Testando o Helios: `python manage.py test`

6 Executando o Helios com visibilidade externa: `python manage.py runserver <meu servidor>:8080`
