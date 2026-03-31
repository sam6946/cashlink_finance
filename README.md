# 🌍 AfriFinance — Plateforme de transfert d'argent en Afrique

Application web Django complète pour les transferts d'argent en Afrique francophone.

---

## 🗂 Architecture du projet

```
afrifinance/
├── afrifinance/          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Application principale
│   ├── migrations/
│   ├── templates/core/
│   │   ├── home.html         # Page d'accueil
│   │   ├── formulaire.html   # Formulaire de demande
│   │   ├── confirmation.html # Page de confirmation
│   │   ├── login.html        # Connexion superuser
│   │   └── dashboard.html    # Dashboard admin
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── base.html         # Template de base (navbar + footer)
├── static/
│   └── css/
│       └── main.css      # Styles principaux
├── manage.py
├── requirements.txt
├── Procfile              # Pour Heroku/Render
├── runtime.txt
└── .env.example
```

---

## ⚡ Installation locale

### 1. Cloner et créer l'environnement virtuel

```bash
git clone https://github.com/votre-repo/afrifinance.git
cd afrifinance

python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditez .env avec vos valeurs
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Créer un superutilisateur (pour le dashboard)

```bash
python manage.py createsuperuser
# Entrez: username, email (optionnel), mot de passe
```

### 6. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Accédez à : http://127.0.0.1:8000

---

## 🔗 URLs importantes

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil |
| `/soumettre/` | Formulaire de demande |
| `/dashboard/` | Dashboard superuser |
| `/dashboard/login/` | Connexion dashboard |
| `/admin/` | Interface admin Django |

---

## 🚀 Déploiement en ligne

### Option A — Render.com (recommandé, gratuit)

1. Créez un compte sur https://render.com
2. Nouveau service → Web Service → connectez votre dépôt GitHub
3. Configurez :
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn afrifinance.wsgi:application`
4. Variables d'environnement à ajouter :
   - `SECRET_KEY` = une clé aléatoire longue
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `votre-app.onrender.com`

### Option B — Heroku

```bash
heroku create afrifinance-app
heroku config:set SECRET_KEY="votre-cle-secrete"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="afrifinance-app.herokuapp.com"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option C — VPS (Ubuntu)

```bash
# Installer Nginx + Gunicorn
sudo apt install nginx python3-pip python3-venv

# Configurer Gunicorn comme service systemd
# Configurer Nginx comme reverse proxy
# Utiliser Let's Encrypt pour HTTPS
```

---

## 🔐 Sécurité

- Les codes secrets sont hashés (SHA-256) avant stockage
- Protection CSRF sur tous les formulaires
- Dashboard accessible aux superusers uniquement
- WhiteNoise pour les fichiers statiques en production
- Validation côté serveur sur tous les champs

---

## 📱 Fonctionnalités

### Page d'accueil
- Hero section avec animation
- Statistiques : 10 000+ transactions, 99,9% réussite, 24/7 support, 0% frais
- Section "Comment ça marche"
- CTA vers le formulaire

### Formulaire de demande
- Nom complet (icône personne)
- Numéro de téléphone (icône téléphone)
- Montant en FCFA (icône cash)
- Code secret masqué (icône cadenas) avec toggle visibilité
- Validation client + serveur
- Loader sur soumission

### Confirmation
- Animation de succès
- Récapitulatif de la demande
- Notification SMS simulée

### Dashboard Superuser
- Statistiques globales (total, en attente, complétées, montant)
- Tableau de toutes les demandes
- Filtres par statut et recherche par nom/téléphone
- Modal de modification du statut et notes admin

---

## 🛠 Technologies

- **Backend**: Python 3.11, Django 4.2
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Fonts**: Bricolage Grotesque + Plus Jakarta Sans
- **Production**: Gunicorn + WhiteNoise
- **Base de données**: SQLite (dev) → PostgreSQL recommandé en prod
