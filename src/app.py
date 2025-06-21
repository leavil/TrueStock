import dash
from dash import html
import dash_bootstrap_components as dbc
from components.sidebar import sidebar

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'TradeSage'

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(dash.page_container, width=10)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
