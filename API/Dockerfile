# Utilisation d'une image officielle de Python
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers de l'API dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel Flask fonctionne
EXPOSE 5050

# Définir la commande de démarrage du conteneur
CMD ["python", "app.py"]