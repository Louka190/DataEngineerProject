from dash import html, dcc

def create_header():
    """
    Function to create the header of the Dash application.
    
    Returns:
        html.Header: A Header component containing the title of the application.
    """
    return html.Header(
        # title of header
        children=[
            dcc.Link(
                html.H1("Spotify Scraper", style={'textDecoration': 'none','textAlign': 'center', 'padding': '10px'}),
                href="/"  # Rediriger vers la page d'accueil
            ),
        ],
        # styles of header
        style={'backgroundColor': 
                '#f8f9fa', 
                'borderBottom': 
                '2px solid #ddd'}
    )
