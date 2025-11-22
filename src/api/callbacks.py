from app import app
from api.serverAPI import ServerAPI
import dash
from dash.dependencies import Input, Output
from dash import html, dcc
import psutil
from pages.dashboard import players_details

api = ServerAPI()
api.connect()
# ~~~~~ Dashboard ~~~~~
@dash.callback(
    Output("details-section", "children"),
    [
        Input("cpu-card", "n_clicks"),
        Input("ram-card", "n_clicks"),
        Input("players-card", "n_clicks")
    ]
)
def dashboard_update_selected_stat(cpu_clicks, ram_clicks, players_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return None
    else:
        selected = ctx.triggered[0]["prop_id"].split("-")[0]

    if selected == "cpu":
        return [html.H3("cpu placeholder")]
    
    elif selected == "ram":
        return [html.H3("ram placeholder")]
    
    elif selected == "players":
        return players_details(api.get_online_players())

# 
@dash.callback(
    [
        Output("cpu-value", "children"),
        Output("cpu-progress", "value"),
        Output("ram-value", "children"),
        Output("ram-progress", "value"),
        Output("disk-value", "children"),
        Output("disk-progress", "value"),
        Output("players-value", "children"),
        Output("ping-value", "children"),
        Output("ph-value", "children")
    ],
    Input("update-interval", "n_intervals")
)
def update_simple_metrics(n):
    sys_stats = api.get_sys_stats()

    players = len(api.get_online_players())
    ping = 23
    ph = 0

    return (
        f"{sys_stats['cpu']}%", sys_stats['cpu'],
        f"{sys_stats['ram']}%", sys_stats['ram'],
        f"{sys_stats['disk']}%", sys_stats['disk'],
        players, 
        ping,
        ph
    )
