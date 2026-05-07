
# Quantium Sales Dashboard - Task 3
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# --- Read from processed_data.csv (Task 2 output) ---
df = pd.read_csv('processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

# --- Build the Dash app ---
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Pink Morsel Sales Dashboard',
            style={'textAlign': 'center'}),

    html.P('Soul Foods Pink Morsel sales before and after the price increase on 15 Jan 2021',
        style={'textAlign': 'center', 'color': 'gray'}),

    dcc.RadioItems(
        id='region-filter',
        options=[
        {'label': 'All Regions', 'value': 'all'},
        {'label': 'North',       'value': 'north'},
        {'label': 'South',       'value': 'south'},
        {'label': 'East',        'value': 'east'},
        {'label': 'West',        'value': 'west'},
        ],
        value='all',
        inline=True,
        style={'textAlign': 'center', 'padding': '10px'}
    ),

    dcc.Graph(id='sales-chart')
])

# --- Callback: update chart when region filter changes ---
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):

    # Filter by region
    if selected_region == 'all':
        filtered = df
    else:
        filtered = df[df['region'] == selected_region]

    # Group by date and sum sales
    grouped = filtered.groupby('date')['sales'].sum().reset_index()

    # Draw line chart
    fig = px.line(
        grouped,
        x='date',
        y='sales',
        title='Pink Morsel Daily Sales — Before vs After Price Increase',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'}
    )

    # Add vertical line marking the price increase date
    fig.add_vline(
        x='2021-01-15',
        line_dash='dash',
        line_color='red',
        annotation_text='Price Increase',
        annotation_position='top left'
    )

    fig.update_layout(
        plot_bgcolor='white',
        hovermode='x unified'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)