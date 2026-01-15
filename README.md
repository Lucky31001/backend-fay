# BACK_FAY (backend)

Petit README minimal pour ce projet Django.

## Description

Backend Django du projet FAY. Contient les commandes Make utiles pour démarrer la base, appliquer les migrations, créer un superuser et lancer le serveur de développement.

## Prérequis

- Python 3.10+ (virtualenv recommandé)
- pip
- PostgreSQL (localement ou via docker-compose)
- (optionnel) expect si vous utilisez la cible `admin-eof` pour préremplir `createsuperuser`

## Installation rapide

```bash
# créer et activer un venv (zsh/bash)
python -m venv .venv
source .venv/bin/activate

# installer les dépendances
make install
```

## Configuration de la base de données

Vous pouvez utiliser `docker compose up -d` (Makefile start-db) ou une base PostgreSQL locale.

Exemple d'env (ou variables dans votre environnement):

- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT

Les réglages Django se trouvent dans `FAYProject/FAY/settings.py`.

## Migrations

```bash
# appliquer les migrations
make migrate
```

## Créer un superuser

Deux options simples :

1) Non-interactif (via Makefile) — KISS :

```bash
# définit les variables d'env puis lance la cible make
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=changeme make admin
```

2) Si vous préférez remplir les invites `createsuperuser` automatiquement (script expect) :

```bash
python FAYProject/manage.py createsuperuser
```

3) Mode interactif (par défaut) :

```bash
make admin
# ou
python FAYProject/manage.py createsuperuser
```

Note : la cible `admin` du Makefile utilise la variable d'environnement si vous la fournissez, sinon elle ouvre l'invite interactive.

## Lancer le serveur

```bash
# lance la DB, applique les migrations puis démarre le serveur (0.0.0.0:8000)
make run

# lancer seulement le serveur de dev (écoute 0.0.0.0:8000)
make start-app
```

## Tests

```bash
make test
```

## Commandes Make utiles

- `make install` — installe les dépendances
- `make run` — démarre la DB, applique les migrations, démarre le serveur
- `make start-db` — démarre la DB via docker compose
- `make migrate` — applique les migrations
- `make admin` — crée un superuser (supporte variables d'env)
- `make admin` — crée un superuser en pilotant `createsuperuser` via expect
- `make start-app` — démarre le serveur dev sur 0.0.0.0:8000
- `make test` — lance la suite de tests

## Dépannage rapide

- Le serveur écoute sur 127.0.0.1 quand vous lancez `python manage.py runserver` sans paramètre. Pour écouter depuis l'extérieur utilisez :

```bash
python FAYProject/manage.py runserver 0.0.0.0:8000
# ou
make start-app
```

