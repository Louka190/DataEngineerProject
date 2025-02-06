from dash import html, dcc

def create_navbar():
    """
    Function to create the navigation bar for the Dash application.
    
    Returns:
        html.Nav: A Nav component containing links for navigation.
    """
    return html.Nav(
        # content of navbar
        children=[
            html.Div(
                dcc.Link("Artistes", href="/artists", style={'color': '#fff', 'textDecoration': 'none'}),
                style={'border': '1px solid white', 'padding': '5px'} 
            ),
            html.Div(
                dcc.Link("Pays", href="/countries", style={'color': '#fff', 'textDecoration': 'none'}),
                style={'border': '1px solid white', 'padding': '5px'} 
            ),
            html.Div(
                dcc.Link("Tendances", href="/toplists", style={'color': '#fff', 'textDecoration': 'none'}),
                style={'border': '1px solid white', 'padding': '5px'}  
            ),
            html.Div(
                dcc.Link("Listeners", href="/listeners", style={'color': '#fff', 'textDecoration': 'none'}),
                style={'border': '1px solid white', 'padding': '5px'} 
            )
        ]
        ,
        # style of navbar 
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'padding': '10px',
            'backgroundColor': '#343a40',
            'color': '#fff'
        }
    )