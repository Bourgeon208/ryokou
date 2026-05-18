# Gaëtan au Japon Django

Blog personnel avec gestion d'articles, commentaires et messages privés.

## Structure

```
blog_project/
├── myblog/          # Configuration Django (settings, urls)
├── blog/            # Application principale
│   ├── models.py    # Post, PostImage, Comment, PrivateMessage
│   ├── views.py     # Vues publiques
│   ├── admin.py     # Panel d'administration
│   ├── forms.py     # Formulaires
│   └── urls.py      # Routes URL
├── templates/       # Templates HTML
│   ├── base.html
│   ├── blog/        # Templates blog
│   └── registration/ # Login / inscription
├── static/css/      # Feuilles de style
├── media/           # Fichiers uploadés (images, vidéos)
├── requirements.txt
├── start.sh         # Script de démarrage
└── manage.py
```

## Installation

### 1. Prérequis
- Python 3.10+

### 2. Démarrage rapide

```bat
cd blog_project

# Option A — Double-clic ou invite de commandes
start.bat

# Option B — PowerShell
.\start.ps1

# Option C — Manuel (invite de commandes ou PowerShell)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Accès

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Blog public |
| http://localhost:8000/admin/ | Panel d'administration |
| http://localhost:8000/inscription/ | Inscription utilisateur |
| http://localhost:8000/contact/ | Envoyer un message privé |
| http://localhost:8000/mes-messages/ | Voir ses messages envoyés |

## Fonctionnalités

### Admin (vous seul)
- Créer des articles avec **texte**, **images multiples**, **vidéo** (fichier ou URL YouTube/Vimeo)
- Gérer les utilisateurs depuis `/admin/auth/user/`
- Modérer les commentaires (approuver / rejeter)
- Lire les messages privés (badge de notification dans la nav)

### Utilisateurs inscrits
- Inscription : username + password uniquement
- Commenter les articles
- Envoyer des messages privés à l'admin
- Voir l'état de ses messages envoyés (lu / non lu)

## Créer un article (depuis l'admin)

1. Aller sur `/admin/blog/post/add/`
2. Remplir le titre → le slug se génère automatiquement
3. Ajouter le contenu
4. Ajouter des images via le panneau inline **Images**
5. Optionnel : uploader une vidéo ou coller une URL YouTube embed
   - URL embed YouTube : `https://www.youtube.com/embed/VIDEO_ID`
6. Cocher **Publié** et sauvegarder

## Personnalisation

- Changer la clé secrète dans `myblog/settings.py` avant la mise en production
- Modifier `DEBUG = False` en production
- Configurer `ALLOWED_HOSTS` avec votre domaine
