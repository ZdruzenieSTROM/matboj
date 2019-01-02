title Matboj

cd %~dp0

SET ENV_NAME=matboj
ENV_NAME\Scripts\activate

py manage.py runserver 0.0.0.0:80
