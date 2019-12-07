import dash_html_components as html
from layouts.stats import layout_stats
from layouts.inputs import layout_inputs
from layouts.visualization import layout_visualization

# Main Layout (Two columns: Inputs / Chart)
main_layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Simple Recommendation Engine [LSH-Base with Jaccord Similarity(MinHash)]")
        ]),
    ], className="row center"),
    html.Div([
        layout_stats
    ], className="row center"),
    html.Div([
        html.Div([
            layout_inputs
        ], className="col-12"),
        html.Div([
            layout_visualization
        ], className="col-8"),
    ], className="row center"),
], className="container")
