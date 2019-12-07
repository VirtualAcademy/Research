import dash_html_components as html
import dash_core_components as dcc

# Input layouts
layout_inputs = html.Div([
    html.H3("Input Text"),
    html.Div(children=[
        # Average
        html.Div(children=[
            dcc.Input(id="input-text", type="text", className="form-control", value="A fast LSH-based similarity search method for multivariate time series", style={"width":"90%"}),
            html.Span(html.Button("search", id='submit-button'))
        ]),
    ], className="row"),
    html.Div(children=[
    html.Div(children=[
        # Permutation
        html.Div(children=[
            html.Label("No. of Permutations"),
            dcc.Input(id="input-perm", type="number", className="form-control center", value=128)
        ])], className="col-6", style={'margin':'2px 10px 20px 20px','float':'left'}),
    html.Div(children=[
        # Recommendation
        html.Div(children=[
            html.Label("No. of Recommendation"),
            dcc.Input(id="input-recom", type="number", className="form-control", value=5)
        ])], className="col-6", style={'margin': '20px 20px auto'}),
], className="row", style={'margin':'auto'}),
])
