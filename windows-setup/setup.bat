title Matboj

cd %~dp0

SET ENV_NAME=matboj

runas /noprofile /user:mymachine\administrator py -m pip install virtualenv
py -m venv ENV_NAME
ENV_NAME\Scripts\activate

runas /noprofile /user:mymachine\administrator py -m pip install -r requirements.txt

py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic

py manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'gumibanan')"

py manage.py runserver 0.0.0.0:80
