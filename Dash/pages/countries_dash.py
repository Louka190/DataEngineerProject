from elasticsearch import Elasticsearch
import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash import Dash

# Initialisation de l'application Dash
app = Dash(__name__)

# Connexion à Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

# Initialisation du scroll avec Elasticsearch
response = es.search(
    index="countries",
    body={
        "query": {
            "match_all": {}  # Récupérer tous les documents
        },
        "size": 1000  # Nombre de résultats par batch dans le corps de la requête
    },
    scroll='2m'  # Durée de vie du scroll
)

# Récupérer le scroll ID
scroll_id = response['_scroll_id']
hits = response['hits']['hits']

data = []

# Extraire les informations de chaque document
while len(hits) > 0:
    for hit in hits:
        data.append(hit['_source'])

    # Effectuer une nouvelle requête de scroll
    response = es.scroll(
        scroll_id=scroll_id,
        scroll='2m'
    )

    # Mettre à jour le scroll ID et les hits
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']

df = pd.DataFrame(data)
countries = df['Country'].unique()

# Créer le menu déroulant
dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in countries],
    placeholder="Sélectionnez un pays"
)

# Layout de la page
layout = html.Div([
    html.H1("Sélectionnez un pays"),
    dropdown,
    html.Div(id='country-output') 
])

def register_callbacks(app):
    # Callback pour afficher les données du pays sélectionné
    @app.callback(
        Output('country-output', 'children'),
        Input('country-dropdown', 'value')
    )
    def display_country_data(selected_country):

        if selected_country is None:
            return html.Div("")

        # Filtrer les données du pays sélectionné
        country_data = df[df['Country'] == selected_country].sort_values(by='Pos')

        # Retourner le tableau des données du pays
        return dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in country_data.columns],
            data=country_data.to_dict('records'),
            style_table={'overflowX': 'auto', 'height': '300px'},  
            style_cell={
                'height': 'auto',
                'minWidth': '0px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }
        )