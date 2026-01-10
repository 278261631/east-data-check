@echo off
C:\Python\Python310\python.exe manage.py migrate --run-syncdb
C:\Python\Python310\python.exe manage.py initadmin
C:\Python\Python310\python.exe manage.py runserver 0.0.0.0:28000

