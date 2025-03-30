# -*- coding: utf-8 -*-
 
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


world_cup_df = pd.read_csv('WinLoss.csv')


winner_counts = world_cup_df['Winner'].value_counts().reset_index()
winner_counts.columns = ['Country', 'Wins']

app = Dash(__name__)

app.layout = html.Div([
    html.H1("World Cup Tracker"),

    html.Div([
        html.H2("Countries that Won the World Cup"),
        dcc.Graph(id='choropleth-map',
                  figure=px.choropleth(winner_counts,
                                       locations='Country',
                                       locationmode='country names',
                                       color='Wins',
                                       title="World Cup Wins by Country",
                                       color_continuous_scale='Viridis')),
    ]),

    html.Div([
        html.H3("Pick Country to View Wins"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in winner_counts['Country']],
            value='Brazil'
        ),
        html.Div(id='country-wins-output')
    ]),

    html.Div([
        html.H3("Pick Year to View Results"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in world_cup_df['Year']],
            value=world_cup_df['Year'].iloc[0]
        ),
        html.Div(id='year-results-output')
    ])
])

@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(country):
    wins_data = winner_counts[winner_counts['Country'] == country]['Wins']
    if wins_data.empty:
        return f"{country} has never won the World Cup."
    else:
        wins = wins_data.values[0]
        return f"{country} has won the World Cup {wins} times."


@app.callback(
    Output('year-results-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_results(year):
    match = world_cup_df[world_cup_df['Year'] == year].iloc[0]
    winner = match['Winner']
    loser = match['Loser']
    return f"In {year}, the winner was {winner}, and the losers were {loser}."

# Run the Dash app
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
