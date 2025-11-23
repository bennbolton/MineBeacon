import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/backups")

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H3("Last backup was on:"),
                                            html.H4("Unknown", id="latest-backup"),
                                            html.H4("Some time ago", id="since-latest-backup")
                                        ]
                                    ),
                                    id="last-backup-card",
                                    className="shadow-sm p-0 h-100"
                                ),
                                width=8
                            ),
                            dbc.Col(
                                html.Div(
                                    dbc.Card(
                                        dbc.CardBody(
                                            html.H2("Backup Now")
                                        ),
                                        className="shadow-sm p-0 h-100"
                                    ),
                                    id="backup-now-button",
                                    n_clicks=0,
                                    style={"cursor": "pointer", "padding": 0, "border": "none"},
                                    
                                ),
                                width=4
                            )
                        ]
                    )
                ]
            )
        ),
        dcc.Location(id="backups-url")
    ],
    fluid=True
)