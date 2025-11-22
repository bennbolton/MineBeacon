from dash import Dash,html, dcc, page_container
import dash_bootstrap_components as dbc
import api.callbacks

# Initialise the app
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.DARKLY],  # nice dark theme
    suppress_callback_exceptions=True
)

app.layout = dbc.Container(
    [
        html.H1("MineBeacon", className="mt-3 mb-3"),

        # Navigation
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("Backups", href="/backups", active="exact"),
                dbc.NavLink("Console", href="/console", active="exact"),
            ],
            pills=True,
        ),

        html.Hr(),

        # This loads the currently selected page
        page_container
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)