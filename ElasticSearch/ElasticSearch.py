import os
import pandas as pd
from elasticsearch import Elasticsearch

# Connexion à Elasticsearch
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
es = Elasticsearch([ES_HOST])

if not es.ping():
    raise ValueError("Impossible de se connecter à Elasticsearch")

# Liste des index à créer et des fichiers CSV associés
INDEXES = {
    "artists": "artists_results.csv",
    "countries": "countries_results.csv",
    "listeners": "listeners_results.csv",
    "toplists": "toplists_results.csv"
}

OUTPUT_DIR = "/app/output"

# Fonction pour importer les CSV dans Elasticsearch
def import_csv_to_elastic(index_name, file_name):
    index_path = os.path.join(OUTPUT_DIR, file_name)
    
    if not os.path.exists(index_path):
        print(f"Erreur : Le fichier {index_path} n'existe pas !")
        return

    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index {index_name} supprimé.")
        
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index {index_name} créé.")

    df = pd.read_csv(index_path)
    for _, row in df.iterrows():
        doc = row.to_dict()
        res = es.index(index=index_name, document=doc)
        print(f"Document ID {res['_id']} indexé dans {index_name}.")
    
    print(f"Tous les documents ont été indexés dans {index_name}.")

# Fonction principale pour importer les données dans les différents index
def import_all_csv_to_elastic():
    for index_name, file_name in INDEXES.items():
        import_csv_to_elastic(index_name, file_name)

if __name__ == "__main__":
    import_all_csv_to_elastic()
