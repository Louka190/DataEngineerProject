FROM python:3.12

# Installer pipenv
RUN pip install pipenv

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers Pipfile et Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Installer les dépendances
RUN pipenv install --deploy --system

# Copier le reste du projet
COPY . /app

# Changer le répertoire de travail pour `project`
WORKDIR /app/project

# Ajouter PYTHONPATH au conteneur
ENV PYTHONPATH=/app/project

# Définir la commande par défaut
CMD ["scrapy", "crawl", "olympics"]
