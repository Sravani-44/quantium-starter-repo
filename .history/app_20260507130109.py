
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

df = pd.read_csv('processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Dashboard'),
    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'All Regions', 'value': 'all'},
            {'label': 'North', 'value': 'north'},
            {'label': 'South', 'value': 'south'},
            {'label': 'East', 'value': 'east'},
            {'label': 'West', 'value': 'west'},
        ],
        value='all',
        inline=True
    ),
    dcc.Graph(id='sales-chart')
])

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered = df
    else:
        filtered = df[df['region'] == selected_region]

    grouped = filtered.groupby('date')['sales'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped['date'],
        y=grouped['sales'],
        mode='lines',
        name='Sales'
    ))

    return fig

if __name__ == '__main__':
    app.run(debug=True)