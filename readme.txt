To setup the project on a new server:
- pip install virtualenv
- virtualenv myenv
- myenv/bin/activate
- git clone
- pip install -r requirements.txt

Setup database
- python manage.py makemigrations (?)
- python manage.py migrate

Run
- python manage.py runserver