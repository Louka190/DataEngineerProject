FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et le script Python
COPY requirements.txt /app/
COPY Mongo.py /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script d'importation
CMD ["python", "Mongo.py"]

