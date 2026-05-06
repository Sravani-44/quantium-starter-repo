
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# --- Load and combine all 3 CSV files ---
df0 = pd.read_csv('data/daily_sales_data_0.csv')
df1 = pd.read_csv('data/daily_sales_data_1.csv')
df2 = pd.read_csv('data/daily_sales_data_2.csv')
df = pd.concat([df0, df1, df2], ignore_index=True)

# --- Clean the data ---
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['date'] = pd.to_datetime(df['date'])
df['sales'] = df['price'] * df['quantity']

# --- Group by date and region ---
summary = df.groupby(['date', 'region'])['sales'].sum().reset_index()

# --- Build the Dash app ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Dashboard'),

    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'All regions', 'value': 'all'},
            {'label': 'North',       'value': 'north'},
            {'label': 'South',       'value': 'south'},
            {'label': 'East',        'value': 'east'},
            {'label': 'West',        'value': 'west'},
        ],
        value='all',
        inline=True
    ),

    dcc.Graph(id='sales-chart')
])

# --- Callback: update chart when region changes ---
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered = summary
    else:
        filtered = summary[summary['region'] == selected_region]

    fig = px.line(
        filtered,
        x='date',
        y='sales',
        color='region',
        title='Daily Sales Over Time'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)