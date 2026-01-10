@echo off
echo Creating virtual environment...
C:\Python\Python310\python.exe -m venv venv
echo Installing dependencies...
call venv\Scripts\activate.bat
pip install django python-decouple django-cors-headers openpyxl
echo Done! Run start.bat to start the server.
pause

