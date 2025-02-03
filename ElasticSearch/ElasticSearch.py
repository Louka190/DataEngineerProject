import os
import pandas as pd
from elasticsearch import Elasticsearch

# Connexion à Elasticsearch
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "artists"

es = Elasticsearch([ES_HOST])

if not es.ping():
    raise ValueError("Impossible de se connecter à Elasticsearch")

if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

OUTPUT_DIR = "/app/output"
ARTISTS_FILE = os.path.join(OUTPUT_DIR, "artists_results.csv")

def import_csv_to_elastic():
    if not os.path.exists(ARTISTS_FILE):
        print(f"Erreur : Le fichier {ARTISTS_FILE} n'existe pas !")
        return

    df = pd.read_csv(ARTISTS_FILE)
    for _, row in df.iterrows():
        doc = row.to_dict()
        res = es.index(index="artists", document=doc)
        print(f"Document ID {res['_id']} indexé.")
    
    print("Tous les documents ont été indexés.")

if __name__ == "__main__":
    import_csv_to_elastic()
