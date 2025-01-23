# DataEngineerProject
Projet de fin d'unité DataEngineerTools de Nathan Lecoin et Louka Morandi 

https://www.olympedia.org/results/19000014



Lorsque vous construisez et exécutez votre configuration Docker Compose, plusieurs étapes se produisent. Voici une explication détaillée de ce qui se passe :

Construction de l'image Docker :

Docker Compose utilise le Dockerfile pour construire une image Docker.
L'image est basée sur python:3.12.
Pipenv est installé pour gérer les dépendances Python.
Les fichiers Pipfile et Pipfile.lock sont copiés dans l'image et les dépendances sont installées.
Le reste du projet est copié dans l'image.
Le répertoire de travail est défini sur /app/project.
La variable d'environnement PYTHONPATH est définie pour inclure /app/project.
Définition des services :

Un service nommé scraper est défini.
Le contexte de construction est défini sur le répertoire courant (.), ce qui signifie que Docker Compose utilisera le Dockerfile à la racine du projet pour construire l'image.
Le conteneur est nommé scraper.
La commande par défaut pour le conteneur est scrapy crawl olympics, ce qui lance le spider Scrapy nommé olympics.

Montage des volumes :

Le répertoire courant (.) est monté dans le conteneur à /app.
Le répertoire ./project/output est monté dans le conteneur à /app/project/output, ce qui permet de partager les fichiers de sortie entre l'hôte et le conteneur.
Définition des variables d'environnement :

SCRAPY_SETTINGS_MODULE est défini sur project.settings, ce qui indique à Scrapy où trouver les paramètres de configuration.
PYTHONPATH est défini sur /app/project pour s'assurer que les modules Python peuvent être trouvés correctement.
Exécution du conteneur :

Docker Compose lance le conteneur scraper.
La commande scrapy crawl olympics est exécutée, ce qui lance le spider Scrapy.
Le spider Scrapy accède à l'URL de départ, extrait les données et les enregistre dans le fichier JSON spécifié (/app/project/output/olympics_results.json).
En résumé, Docker Compose automatise la construction de l'image Docker, la configuration des services, le montage des volumes et l'exécution des commandes nécessaires pour lancer votre projet Scrapy dans un environnement conteneurisé.