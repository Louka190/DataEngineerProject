import os
from elasticsearch import Elasticsearch, helpers
import json

# Connexion à ElasticSearch
es = Elasticsearch("http://localhost:9200")

# Calculer le chemin relatif à partir du répertoire courant
base_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(base_dir, "project", "olympics_results.json")

# Vérifier si le fichier existe
if os.path.exists(json_file):
    print(f"Le fichier JSON est trouvé à : {json_file}")
else:
    print(f"Le fichier JSON est introuvable à : {json_file}")
    exit(1)  # Arrêter le script si le fichier n'est pas trouvé

# Index cible
index_name = "jo_100m_swimming"

# Charger les données JSON
try:
    with open(json_file, "r") as f:
        json_data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Erreur de décodage JSON : {e}")
    exit(1)

# Extraire les enregistrements sous la clé "Data"
data = json_data.get("Data", [])

# Préparer les données pour ElasticSearch
actions = [
    {
        "_index": index_name,
        "_source": record
    }
    for record in data
]

# Insérer les données dans ElasticSearch et afficher les erreurs si elles surviennent
try:
    success, failed = helpers.bulk(es, actions, raise_on_error=False)
    if failed:
        print(f"{len(failed)} documents ont échoué à l'indexation.")
        print(f"Erreurs : {failed}")
    else:
        print(f"Toutes les données ont été insérées avec succès dans l'index '{index_name}' !")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")