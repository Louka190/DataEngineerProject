import os
import pandas as pd
from pymongo import MongoClient

# Connexion à MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "scrapy_data")

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

# Dossier où sont stockés les CSV (correction du chemin)
OUTPUT_DIR = "/app/output"

def import_csv_to_mongo():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Erreur : Le dossier {OUTPUT_DIR} n'existe pas !")
        return

    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(OUTPUT_DIR, file)
            collection_name = file.replace("_results.csv", "") 
            df = pd.read_csv(file_path)

            # Insertion des données dans MongoDB
            db[collection_name].insert_many(df.to_dict(orient="records"))
            print(f"Importé {file} dans MongoDB, collection: {collection_name}")

if __name__ == "__main__":
    import_csv_to_mongo()
