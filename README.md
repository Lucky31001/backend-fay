# Command to use

## Python

```bash
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	django-admin --version	
```

## Config a SuperUltraBigUser for /admin/ ( CD dans le dossier FAYProject)

```bash
    python manage.py createsuperuser
```

## Run the server

```bash
    cd FAYProject
    python manage.py runserver
```

## Config DB

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ma_db',
        'USER': 'mon_user',
        'PASSWORD': 'motdepassefort',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
