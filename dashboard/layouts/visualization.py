import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

# Visualization Layout
layout_visualization = html.Div([
    html.H3("Recommendations: Similar Conference Papers"),
    # Element to output plotly chart
    dcc.Loading(
        id="loading-1", 
        children=[
            dt.DataTable(
                id='output-table',
                columns=[
                    {"name":i, "id":i} for i in ["Number", "Titles"]
                    ],
                style_cell={'textAlign': 'center'})
                ], type="default"),
    
    html.H3("Visualization"),
    # Element to output plotly chart
    dcc.Graph(id='output-data-1'),
    # Element to output plotly chart
    dcc.Graph(id='output-data-2')
], style={'margin':'auto'})
