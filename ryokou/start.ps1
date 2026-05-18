# Script de demarrage — Gaëtan au Japon Django
# Executer avec : .\start.ps1

Write-Host "`n Installation des dependances..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "`n Creation de la base de donnees..." -ForegroundColor Cyan
python manage.py migrate

Write-Host "`n Creation du compte administrateur..." -ForegroundColor Cyan
Write-Host " (Ce compte vous donnera acces au panel /admin/)" -ForegroundColor Gray
python manage.py createsuperuser

Write-Host "`n Lancement du serveur..." -ForegroundColor Green
Write-Host "  -> http://localhost:8000" -ForegroundColor White
Write-Host "  -> http://localhost:8000/admin/" -ForegroundColor White
Write-Host ""
python manage.py runserver
