from dash import html 

def create_footer():
    """
    Function to create the footer of the Dash application.
    
    Returns:
        html.Footer: A Footer component containing footer content.
    """
    return html.Footer(
        # content of footer
        children=[
            html.Div("Scraper Spotify", style={'textAlign': 'center', 'padding': '10px'}),
            html.Div("MORANDI Louka & LECOIN Nathan", style={'textAlign': 'center', 'padding': '5px'}),
        ],
        # style of footer
        style={
            'backgroundColor': '#343a40',  # Background color of the footer
            'color': '#fff',  # Text color
            'position': 'relative',  # Positioning the footer
            'bottom': '0',  # Align to the bottom
            'width': '100%',  # Full width
            'padding': '10px',  # Padding inside the footer
        }
    )
