#!/bin/bash
dropdb helios -h localhost -U postgres
createdb helios -h localhost -U postgres
python manage.py syncdb
python manage.py migrate
#echo "from helios_auth.models import User; User.objects.create(user_type='google',user_id='dfaranha@gmail.com', info={'name':'Diego F. Aranha'})" | python manage.py shell
