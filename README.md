# Command to use

## Python

```bash
	python -m venv .venv
	source .venv/bin/activate OR .venv\Scripts\Activate.ps1
	make install
	django-admin --version	
```
## Run the server

```bash
    make run
```

## Config a SuperUltraBigUser for /admin/

```bash
	make admin
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
