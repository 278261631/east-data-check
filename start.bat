@echo off
call venv\Scripts\activate.bat
python manage.py migrate --run-syncdb
python manage.py initadmin
python manage.py runserver 0.0.0.0:28000

