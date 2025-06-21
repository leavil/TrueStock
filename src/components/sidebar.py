# src/components/sidebar.py
import dash_bootstrap_components as dbc

sidebar = dbc.Nav(
    [
        dbc.NavLink("Dashboard", href="/", active="exact"),
        dbc.NavLink("Valuación", href="/valuation", active="exact"),
        dbc.NavLink("Portafolio", href="/portfolio", active="exact"),
        dbc.NavLink("Alertas", href="/alerts", active="exact"),
    ],
    vertical=True,
    pills=True,
    className="bg-light"
)
