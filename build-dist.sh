#!/bin/bash

# Vytvorí zipko s nastaveným serverom a skriptom čo ho spustí na 64-bitových? linuxoch

mkdir dist
cp -r competition matboj manage.py requirements.txt dist/
cd dist

rm -r competition/__pycache__
rm -r competition/migrations/*
touch competition/migrations/__init__.py
rm -r matboj/__pycache__

echo -e "#!/bin/bash\nsource environment/bin/activate\npython3 manage.py runserver 0.0.0.0:8000\ndeactivate" > run.sh
chmod +x run.sh

python3 -m virtualenv --python=$(which python3) environment
source environment/bin/activate

pip3 install -r requirements.txt

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'gumibanan')"

deactivate

cd ..

zip -r dist.zip dist

rm -r dist
