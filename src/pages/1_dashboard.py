# src/pages/1_dashboard.py

import dash
import dash_bootstrap_components as dbc
dash.register_page(__name__, path='/')

from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
from utils.fmp import get_ratios

layout = html.Div([
    html.H2("Análisis de Tickers", className="mt-4"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': t, 'value': t} for t in ['AAPL', 'MSFT', 'GOOG', 'MCD', 'TSLA']],
        value='AAPL',
        placeholder="Selecciona un ticker"
    ),
    dcc.RadioItems(
    id='range-selector',
    options=[
        {'label': 'MAX', 'value': 'max'},
        {'label': '5Y', 'value': '5y'},
        {'label': '1Y', 'value': '1y'},
        {'label': '6M', 'value': '6mo'},
        {'label': '3M', 'value': '3mo'},
        {'label': '1M', 'value': '1mo'},
        {'label': '1W', 'value': '5d'},
        {'label': '1D', 'value': '1d'}
    ],
    value='6mo',
    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
    className='my-2'
    ),
     dcc.RadioItems(
        id='chart-type',
        options=[
            {'label': 'Línea', 'value': 'line'},
            {'label': 'Velas', 'value': 'candlestick'}
        ],
        value='candlestick',
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        className="my-3"
    ),
     

    html.Div(id='ratios-output', className="my-3"),
    dcc.Graph(id='price-volume-chart')
])

@callback(
    Output('price-volume-chart', 'figure'),
    Output('ratios-output', 'children'),
    Input('ticker-dropdown', 'value'),
    Input('chart-type', 'value'),
    Input('range-selector', 'value')  # ⬅️ Nuevo input
)
def update_dashboard(ticker, chart_type, period):
    if not ticker:
        return go.Figure(), ""

    df = yf.download(ticker, period=period, auto_adjust=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
        return go.Figure(), html.Div("Datos incompletos para graficar.", style={"color": "red"})

    fig = go.Figure()

    # 🔁 Tipo de gráfico
    if chart_type == 'line':
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Precio',
            line=dict(color='blue')
        ))
    else:
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Velas'
        ))

    # Volumen
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volumen',
        yaxis='y2',
        opacity=0.3,
        marker=dict(color='rgba(100, 100, 200, 0.4)')
    ))

    fig.update_layout(
        title=f'{ticker} - {period.upper()} - {"Velas" if chart_type == "candlestick" else "Línea"}',
        yaxis=dict(title='Precio'),
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title='Volumen'
        ),
        xaxis_rangeslider_visible=(chart_type == 'candlestick'),
        hovermode='x unified'
    )

    try:
        ratios = get_ratios(ticker)
        pe = round(float(ratios[0]['peRatioTTM']), 2)
        roe = round(float(ratios[0]['returnOnEquityTTM']) * 100, 2)
        roa = round(float(ratios[0]['returnOnAssetsTTM']) * 100, 2)

        ratios_html = html.Ul([
            html.Li(f"PE Ratio: {pe}"),
            html.Li(f"ROE: {roe}%"),
            html.Li(f"ROA: {roa}%"),
        ])
    except Exception as e:
        ratios_html = html.Div(f"Error al obtener ratios: {str(e)}", style={"color": "red"})

    return fig, ratios_html

