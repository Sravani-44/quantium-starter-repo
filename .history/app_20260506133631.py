
# Quantium Sales Dashboard - Task 3
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# --- Read from processed_data.csv ---
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

    # Draw line chart using graph_objects
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped['date'],
        y=grouped['sales'],
        mode='lines',
        name='Sales',
        line=dict(color='blue')
    ))

    # Add vertical line for price increase date
    fig.add_shape(
        type='line',
        x0='2021-01-15', x1='2021-01-15',
        y0=0, y1=1,
        yref='paper',
        line=dict(color='red', dash='dash', width=2)
    )

    # Add label for the vertical line
    fig.add_annotation(
        x='2021-01-15',
        y=1,
        yref='paper',
        text='Price Increase',
        showarrow=False,
        font=dict(color='red'),
        xanchor='left'
    )

    fig.update_layout(
        title='Pink Morsel Daily Sales — Before vs After Price Increase',
        xaxis_title='Date',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='white',
        hovermode='x unified'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)