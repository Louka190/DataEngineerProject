import os
import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input
from src.components.header import create_header
from src.components.navbar import create_navbar 
from src.components.footer import create_footer

from pages.countries_dash import layout as countries_layout, register_callbacks

# Initialiser l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True)

# Layout de l'application Dash
app.layout = html.Div(children=[
    create_header(),
    create_navbar(),
    create_footer(),
    dcc.Location(id='url', refresh=False),  # Écoute des changements d'URL
    html.Div(id='page-content'),  # Contenu dynamique en fonction de l'URL
])

# Enregistrer les callbacks
register_callbacks(app)

# Callback pour gérer l'affichage de la page en fonction de l'URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/countries':  # Si l'URL correspond à /countries
        return countries_layout  # Charger le layout des pays
    else:
        # Par défaut, afficher la page d'accueil
        return html.Div([
            html.H1("Bienvenue sur mon site"),
            html.P("Ceci est un exemple d'application Dash."),
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
