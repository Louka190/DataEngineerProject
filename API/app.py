from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import io
import base64

matplotlib.use("Agg")

app = Flask(__name__)

# Liste des index pour la navbar
indices = ['artists', 'countries', 'toplists', 'listeners']

# Connexion à Elasticsearch
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elastic:9200")
es = Elasticsearch(ELASTICSEARCH_HOST)

@app.route('/')
def home():
    """
    Page de présentation (aucun appel à Elasticsearch).
    """
    description = (
        "Bienvenue sur le dashboard de Spotify Scraper.<br>"
        "Utilisez la barre de navigation ci-dessus pour accéder aux données de chaque index."
    )
    return render_template('index.html', title="Spotify Scraper", description=description, indices=indices)


@app.route('/artists', methods=['GET', 'POST'])
def artists():
    """
    Recherche d'artistes dans l'index 'artists'.
    """
    results = []
    searched_name = None

    if request.method == 'POST':
        searched_name = request.form.get('artist_name')

        query = {
            "query": {
                "match": {
                    "Artist": searched_name
                }
            }
        }
        response = es.search(index='artists', body=query)
        results = response.get('hits', {}).get('hits', [])

    return render_template(
        'artists.html',
        title="Spotify Scraper",
        indices=indices,
        results=results,
        searched_name=searched_name
    )


@app.route('/artist/<doc_id>')
def show_artist_details(doc_id):
    """
    Affiche les détails d'un artiste via son ID Elasticsearch.
    """
    try:
        doc = es.get(index='artists', id=doc_id)
        return render_template(
            'artist_detail.html',
            title="Spotify Scraper",
            indices=indices,
            doc=doc
        )
    except Exception as e:
        return f"Erreur lors de la récupération des données : {str(e)}", 404


@app.route('/countries', methods=['GET', 'POST'])
def countries():
    """
    Recherche et affichage des données pour un pays spécifique.
    """
    results = []
    searched_country = None

    country_query = {
        "size": 0,
        "aggs": {
            "unique_countries": {
                "terms": {
                    "field": "Country.keyword",
                    "size": 200
                }
            }
        }
    }
    country_response = es.search(index='countries', body=country_query)
    countries = sorted([bucket['key'] for bucket in country_response['aggregations']['unique_countries']['buckets']])

    if request.method == 'POST':
        searched_country = request.form.get('country_name')

        query = {
            "query": {
                "match": {
                    "Country": searched_country
                }
            },
            "size": 50,
            "sort": [
                {"Pos": {"order": "asc"}}
            ]
        }
        response = es.search(index='countries', body=query)
        results = response.get('hits', {}).get('hits', [])

    return render_template(
        'countries.html',
        title="Spotify Scraper",
        indices=indices,
        countries=countries,
        results=results,
        searched_country=searched_country
    )

@app.route('/listeners')
def listeners():
    """
    Génère un bar chart des 40 artistes avec le plus de listeners.
    """
    query = {
        "size": 40, 
        "query": {"match_all": {}},  
        "sort": [{"Listeners": {"order": "desc"}}],  
        "_source": ["Artist", "Listeners"]
    }
    response = es.search(index='listeners', **query)
    hits = response.get('hits', {}).get('hits', [])

    # Vérification si Elasticsearch retourne des données
    if not hits:
        print("Aucune donnée récupérée depuis Elasticsearch.")
        return render_template('listeners.html', title="Spotify Scraper", indices=indices, image_uri=None)

    # Extraction des données en DataFrame Pandas
    data = []
    for hit in hits:
        artist = hit['_source']['Artist'][0] if isinstance(hit['_source']['Artist'], list) else hit['_source']['Artist']
        listeners = hit['_source']['Listeners'] if isinstance(hit['_source']['Listeners'], int) else int(hit['_source']['Listeners'])
        data.append([artist, listeners])

    df = pd.DataFrame(data, columns=['Artist', 'Listeners'])


    fig, ax = plt.subplots(figsize=(14, 8)) 
    df.sort_values(by="Listeners", ascending=False, inplace=True)

    ax.bar(df['Artist'], df['Listeners'], color='dodgerblue', edgecolor='black', linewidth=1.2)
    ax.set_xlabel("Artistes", fontsize=12, fontweight='bold')
    ax.set_ylabel("Nombre d'auditeurs mensuels", fontsize=12, fontweight='bold')
    #ax.set_title("Top 40 Artistes par Nombre de Listeners", fontsize=14, fontweight='bold', pad=15)
    ax.set_xticklabels(df['Artist'], rotation=45, ha="right", fontsize=10) 
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x/1_000_000)}M"))  
    ax.grid(axis='y', linestyle="--", alpha=0.7)

    # Sauvegarde du graphique dans un buffer mémoire
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)

    # Encode l’image en base64
    encoded_image = base64.b64encode(buf.getvalue()).decode("utf-8")
    image_uri = f"data:image/png;base64,{encoded_image}"

    return render_template('listeners.html', title="Spotify Scraper", indices=indices, image_uri=image_uri)

@app.route('/toplists', methods=['GET', 'POST'])
def toplists():
    """
    Recherche et affichage des données pour une catégorie (Category) spécifique 
    dans l'index 'toplists', avec pagination limitée à 20 pages.
    """
    results = []
    searched_category = None
    page = int(request.args.get('page', 1))  # Récupération du numéro de page (par défaut 1)
    offset = (page - 1) * 50                 # Calcul de l'offset basé sur la page
    total_results = 0                         # Initialisation du nombre total de résultats

    # Requête d'agrégation pour récupérer la liste unique des Category
    category_query = {
        "size": 0,
        "aggs": {
            "unique_categories": {
                "terms": {
                    "field": "Category.keyword",
                    "size": 200
                }
            }
        }
    }
    category_response = es.search(index='toplists', body=category_query)
    categories = sorted([bucket['key'] for bucket in category_response['aggregations']['unique_categories']['buckets']])

    if request.method == 'POST':
        searched_category = request.form.get('category_name')
    else:
        searched_category = request.args.get('category_name')

    if searched_category:
        # Requête Elasticsearch avec pagination et récupération du total de résultats
        query = {
            "query": {
                "term": {
                    "Category.keyword": searched_category
                }
            },
            "from": offset,
            "size": 50,
            "sort": [
                {"Position": {"order": "asc"}}
            ],
            "track_total_hits": True  # Permet de récupérer le nombre total de résultats
        }
        response = es.search(index='toplists', body=query)
        results = response.get('hits', {}).get('hits', [])
        total_results = response.get('hits', {}).get('total', {}).get('value', 0)  # Nombre total de résultats

    # Calcul du nombre total de pages, limité à 20
    total_pages = min((total_results // 50) + (1 if total_results % 50 > 0 else 0), 20)

    return render_template(
        'toplists.html',
        title="Spotify Scraper",
        indices=indices,
        categories=categories,
        results=results,
        searched_category=searched_category,
        current_page=page,
        total_pages=total_pages
    )


@app.route('/<index_name>')
def show_index(index_name):
    """
    Route générique pour afficher les 10 premiers éléments des autres index.
    """
    if index_name not in indices:
        return "Index non valide", 404

    query = {
        "query": {"match_all": {}},
        "size": 10
    }
    response = es.search(index=index_name, body=query)
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)