#!/bin/bash

# Vytvorí zipko s nastaveným serverom a skriptom čo ho spustí na 64-bitových? linuxoch

cd "$(dirname "$0")"

DIST_NAME="server"
ENV_NAME="pyenv"

mkdir $DIST_NAME
cp -r competition matboj manage.py requirements.txt $DIST_NAME/
cd $DIST_NAME

rm -r competition/__pycache__ competition/migrations/* matboj/__pycache__
touch competition/migrations/__init__.py

echo -e "#!/bin/bash\ncd \"\$(dirname \"\$0\")\"\nsource "$ENV_NAME"/bin/activate\npython3 manage.py runserver 0.0.0.0:8000\ndeactivate" > run.sh
chmod +x run.sh

python3 -m virtualenv --python=$(which python3) $ENV_NAME
source $ENV_NAME/bin/activate

pip3 install -r requirements.txt

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'gumibanan')"

deactivate

cd ..

zip -r $DIST_NAME.zip $DIST_NAME

rm -r $DIST_NAME
