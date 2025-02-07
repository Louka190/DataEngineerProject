from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Liste des index pour la navbar
indices = ['artists', 'countries', 'toplists', 'listeners']

@app.route('/')
def home():
    """
    Page de présentation (aucun appel à Elasticsearch).
    """
    description = (
        "Bienvenue sur le dashboard de Spotify Scraper.<br>"
        "Ceci est une page de présentation. Utilisez la barre de navigation ci-dessus pour accéder aux données de chaque index."
    )
    return render_template('index.html', title="spotify scraper", description=description, indices=indices)

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    """
    Onglet spécifique pour la recherche d'artistes dans l'index 'artists'.
    """
    es = Elasticsearch("http://localhost:9200")

    if request.method == 'POST':
        # Nom de l'artiste saisi dans le formulaire
        artist_name = request.form.get('artist_name')

        # Requête ES : on cherche dans le champ "Artist" de l'index "artists"
        query = {
            "query": {
                "match": {
                    "Artist": artist_name
                }
            }
        }
        response = es.search(index='artists', body=query)
        # Les hits contiennent habituellement "_source"
        results = response.get('hits', {}).get('hits', [])
        
        return render_template(
            'artists.html',
            title="spotify scraper",
            indices=indices,
            results=results,
            searched_name=artist_name
        )
    else:
        # En GET, page de recherche vide
        return render_template(
            'artists.html',
            title="spotify scraper",
            indices=indices,
            results=None,
            searched_name=None
        )

@app.route('/artist/<doc_id>')
def show_artist_details(doc_id):
    """
    Affiche TOUS les champs d'un artiste précis, via son doc_id.
    """
    es = Elasticsearch("http://localhost:9200")
    
    # Récupération du document par son ID.
    # Par défaut, es.get() renvoie un dictionnaire avec '_source', '_id', etc.
    doc = es.get(index='artists', id=doc_id)
    # doc['_source'] contiendra l'ensemble de vos champs.
    
    return render_template(
        'artist_detail.html',
        title="spotify scraper",
        indices=indices,
        doc=doc
    )

@app.route('/<index_name>')
def show_index(index_name):
    """
    Route générique pour les autres index : countries, toplist, listeners.
    """
    if index_name not in indices:
        return "Index non valide", 404

    es = Elasticsearch("http://localhost:9200")
    
    query = {
        "query": {"match_all": {}},
        "size": 10
    }
    response = es.search(index=index_name, body=query)
    
    # Simplement renvoyer le JSON pour exemple
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
