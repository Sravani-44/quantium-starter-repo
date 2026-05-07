
# Quantium Pink Morsel Sales Dashboard - Task 4
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# --- Load processed data ---
df = pd.read_csv('processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f8f9fa',
        'minHeight': '100vh',
        'padding': '0'
    },
    children=[

        # Header banner
        html.Div(
            style={
                'backgroundColor': '#d62728',
                'padding': '24px 40px',
                'marginBottom': '24px'
            },
            children=[
                html.H1(
                    'Pink Morsel Sales Dashboard',
                    style={
                        'color': 'white',
                        'margin': '0',
                        'fontSize': '28px',
                        'fontWeight': 'bold'
                    }
                ),
                html.P(
                    'Soul Foods — Impact of the Pink Morsel price increase on 15 January 2021',
                    style={
                        'color': '#ffcccc',
                        'margin': '6px 0 0',
                        'fontSize': '14px'
                    }
                )
            ]
        ),

        # Main content
        html.Div(
            style={'padding': '0 40px 40px'},
            children=[

                # Filter section
                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'borderRadius': '8px',
                        'padding': '20px 24px',
                        'marginBottom': '20px',
                        'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.Label(
                            'Filter by Region:',
                            style={
                                'fontWeight': 'bold',
                                'fontSize': '14px',
                                'color': '#333',
                                'marginBottom': '12px',
                                'display': 'block'
                            }
                        ),
                        dcc.RadioItems(
                            id='region-filter',
                            options=[
                                {'label': ' All Regions', 'value': 'all'},
                                {'label': ' North',       'value': 'north'},
                                {'label': ' South',       'value': 'south'},
                                {'label': ' East',        'value': 'east'},
                                {'label': ' West',        'value': 'west'},
                            ],
                            value='all',
                            inline=True,
                            style={'fontSize': '14px', 'color': '#555'},
                            inputStyle={'marginRight': '6px', 'marginLeft': '16px'}
                        )
                    ]
                ),

                # Chart section
                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'borderRadius': '8px',
                        'padding': '20px 24px',
                        'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
                    },
                    children=[
                        dcc.Graph(id='sales-chart')
                    ]
                )
            ]
        )
    ]
)

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
        name='Sales',
        line=dict(color='#d62728', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(214,39,40,0.08)'
    ))

    # Vertical line for price increase
    fig.add_shape(
        type='line',
        x0='2021-01-15', x1='2021-01-15',
        y0=0, y1=1,
        yref='paper', xref='x',
        line=dict(color='#333', dash='dash', width=1.5)
    )

    fig.add_annotation(
        x='2021-01-15',
        y=0.98,
        yref='paper', xref='x',
        text='Price Increase — Jan 15, 2021',
        showarrow=False,
        font=dict(color='#333', size=11),
        xanchor='left',
        bgcolor='white',
        bordercolor='#ccc',
        borderwidth=1
    )

    fig.update_layout(
        title=dict(
            text='Pink Morsel Daily Sales — Before vs After Price Increase',
            font=dict(size=16, color='#222')
        ),
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            title='Total Sales ($)',
            showgrid=True,
            gridcolor='#f0f0f0'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=60, b=60, l=60, r=40)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)