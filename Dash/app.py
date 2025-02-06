import os
import pandas as pd
import dash

from elasticsearch import Elasticsearch
from dash import Dash, html, dcc, callback, Output, Input  
from src.components.header import create_header  
from src.components.navbar import create_navbar 
from src.components.footer import create_footer

# Initialiser l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True)


# Créer un contenu dynamique pour afficher les données récupérées
def create_data_display(data):
    return html.Div([
        html.H3("Données provenant d'Elasticsearch"),
        html.Ul([
            html.Li(f"ID: {doc['_id']}, Score: {doc['_score']}, Source: {doc['_source']}")
            for doc in data
        ])
    ])

# Layout de l'application Dash
app.layout = html.Div(children=[
    create_header(),
    create_navbar(),
    create_footer(),
    dcc.Location(id='url', refresh=False),  
    html.Div(id='page-content'),  
    html.H1("Bienvenue sur mon site"),
    html.P("Ceci est un exemple d'application Dash."),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
