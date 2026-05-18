@echo off
echo.
echo  Installation des dependances...
pip install -r requirements.txt

echo.
echo  Creation de la base de donnees...
python manage.py migrate

echo.
echo  Creation du compte administrateur...
echo  (Ce compte vous donnera acces au panel /admin/)
python manage.py createsuperuser

echo.
echo  Lancement du serveur...
echo  -^> http://localhost:8000
echo  -^> http://localhost:8000/admin/
echo.
python manage.py runserver
pause
