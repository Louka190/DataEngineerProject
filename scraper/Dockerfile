FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le Pipfile et le Pipfile.lock depuis la racine du projet
COPY Pipfile /app/
COPY Pipfile.lock /app/

# Copier les fichiers de l'application
COPY . /app

# Installer pipenv
RUN pip install --no-cache-dir pipenv

# Spécifier la version de Python à utiliser avec pipenv
RUN pipenv --python 3.12

# Installer les dépendances à partir du Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Vérifier l'installation de scrapy
RUN pipenv run scrapy --version

# Commande par défaut pour exécuter toutes les spiders
CMD ["sh", "-c", "cd /app/scraper && pipenv run scrapy crawl artists -s SCRAPY_SETTINGS_MODULE=scraper.settings && pipenv run scrapy crawl countries -s SCRAPY_SETTINGS_MODULE=scraper.settings && pipenv run scrapy crawl listeners -s SCRAPY_SETTINGS_MODULE=scraper.settings"]
