import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/console")

layout = dbc.Container(
    [
        html.H2("Server Console"),
        dcc.Textarea(
            id="console-output",
            style={"width": "100%", "height": "300px"},
            readOnly=True,
        ),
        html.Br(),
        dbc.Input(id="console-input", placeholder="Enter command..."),
        html.Br(),
        dbc.Button("Send", id="send-command", color="primary"),
    ]
)