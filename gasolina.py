"""
Análise de dados de consumo de gasolina no Brasil
Autor: Wesin Ribeiro
Data: 31 julho 2022
"""
import pandas as pd
import json
import plotly.express as px
import dash
from dash import dcc
from dash import html


def load_data():
    """Carrega dados do arquivo csv."""
    ca202102 = pd.read_csv(
        'ca-2021-02.csv',
        encoding="ISO-8859-1",
        sep=';'
    )
    venda = pd.to_numeric(
        ca202102['Valor de Venda'].str.replace(',', '.')
    )
    ca202102['Valor de Venda'] = venda
    gasolina = ca202102.query("Produto == 'GASOLINA' or Produto == \
        'GASOLINA ADITIVADA'")
    gasolina = gasolina.drop(columns=['Valor de Compra'])
    gasolina_estado = gasolina.groupby(
        ['Estado - Sigla'],
        as_index=False
    ).mean()
    return gasolina_estado


def create_plot(gasolina_estado):
    """Cria gráfico de barras."""
    json_states = json.load(open('geojson/brasil_estados.json'))
    fig = px.choropleth(
        gasolina_estado,
        geojson=json_states,
        locations='Estado - Sigla',
        color='Valor de Venda',
        color_continuous_scale="Reds",
        range_color=(4, 7),
        scope='south america',
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def create_dashboard(fig):
    """Cria dashboard."""
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.H1(children='Preço médio da gasolina por estado.'),

        html.P(children='''
            Os dados foram retirados do portal Dados.gov e compreende \
                os valores da gasolina do ano de 2021.'''),
        html.P(children='''
            Infelizmente, não foi possível agrupar por município, pois \
                não há dados disponíveis.'''),

        dcc.Graph(
            id='Choropleth',
            figure=fig
        )
    ])
    return app


def main():
    """Executa o programa."""
    gasolina_estado = load_data()
    fig = create_plot(gasolina_estado)
    app = create_dashboard(fig)
    app.run_server(debug=True, use_reloader=False)


main()
