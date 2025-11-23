from app import app
from api.serverAPI import ServerAPI
import dash
from dash.dependencies import Input, Output
from dash import html, dcc
import psutil
from pages.dashboard import players_details
import os
import datetime

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
    Input("metric-update-interval", "n_intervals")
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

@dash.callback(
    [
        Output("latest-backup", "children"),
        Output("since-latest-backup", "children")
    ],
    Input("backups-url", "pathname")
)
def update_backups(_):
    dt = api.get_latest_backup_datetime()
    niceStr = dt.strftime("%d %B %Y at %H:%M:%S")
    delta = datetime.datetime.now() - dt

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    timeSince = ""
    if minutes < 1:
        timeSince = "Just now"
    else:
        if days > 0:
            timeSince += f"{days} day{'' if days == 1 else 's'}, "
        if hours > 0:
            timeSince += f"{hours} hour{'' if hours == 1 else 's'} and "
        timeSince += f"{minutes} minute{'' if minutes == 1 else 's'} ago"
    return (niceStr,timeSince)

@dash.callback(
    Input("backup-now-button", "n_clicks")
)
def make_new_backup(_):
    api.make_backup()