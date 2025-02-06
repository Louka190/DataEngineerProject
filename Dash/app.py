import dash
from dash import Dash, html, dcc, callback, Output, Input  
from src.components.header import create_header  
from src.components.navbar import create_navbar 
from src.components.footer import create_footer 

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    create_header(),
    create_navbar(),
    create_footer(),
    dcc.Location(id='url', refresh=False),  
    html.Div(id='page-content'),  
    html.H1("Bienvenue sur mon site"),
    html.P("Ceci est un exemple d'application Dash.")
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)