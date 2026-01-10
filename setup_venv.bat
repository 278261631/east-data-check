@echo off
echo Creating virtual environment...
python.exe -m venv venv
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install django python-decouple django-cors-headers openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
echo Done! Run start.bat to start the server.
pause

