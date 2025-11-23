import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

def metric_card(id_base, title, hasProgress = False):
    return html.Div(
        dbc.Card(
            [
                dbc.CardHeader(title, className="text-center fw-bold"),
                dbc.CardBody(
                    [
                        html.H3("", className="text-center", id=f"{id_base}-value"),
                        dbc.Progress(0, striped=False, animated=False, className="mt-2", id=f"{id_base}-progress") if hasProgress else None
                    ]
                )
            ],
            className="shadow-sm p-0 h-100",
        ),
        id=f"{id_base}-card",
        n_clicks=0,
        style={"cursor": "pointer", "padding": 0, "border": "none"},
    )

# ~~~~ Layout ~~~~
layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2("System Overview"),
                    dbc.Row(
                        [
                            dbc.Col(metric_card("players", "Players Online"), width=4),
                            dbc.Col(metric_card("ping", "Ping"), width=4),
                            dbc.Col(metric_card("ph", "Placeholder"), width=4)   
                            
                        ],
                        className="mb-4 g-3"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(metric_card("cpu", "CPU Usage", hasProgress=True), width=4),
                            dbc.Col(metric_card("ram", "RAM Usage", hasProgress=True), width=4),
                            
                            dbc.Col(metric_card("disk", "Disk Usage", hasProgress=True), width=4),
                                         
                        ],
                        className="g-3"
                    )
                ]
            ),
            className="p-4 shadow rounded-4 mt-4"
        ),
        html.Hr(className="my-4"),
        html.Div(id="details-section"),
        dcc.Interval(id="metric-update-interval", interval=5000, n_intervals=0)
    ],
    fluid=True
)

# Players Section
def players_details(online_players):
    player_cards = []
    for player in online_players:
        card = dbc.Col(dbc.Card(
            [
                dbc.CardHeader(player, className="text-center fw-bold"),
            ],
            className="shawdow-sm h-100",
            style={"minHeight": "150px"}
                
            ),
            width=4,
            className="mb-3"
        )
        player_cards.append(card)

    rows = []
    for i in range(0, len(player_cards), 3):
        row = dbc.Row(player_cards[i:i+3], className="mb-3 g-3")
        rows.append(row)

    container = dbc.Card(
        dbc.CardBody(
            rows
        ),
        className="p-3 shadow rounded-3"
    )
    return [container] 