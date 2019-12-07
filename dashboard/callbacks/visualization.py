import numpy as np
import pandas as pd
from server import app
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
# To display the figure defined by this dict, use the low-level plotly.io.show function
import plotly.io as pio
from callbacks.data import db
from callbacks.recommendation import Forest, Rengine, get_timing, calculate_duration, print_message

# Some globals

CAL = lambda t: calculate_duration(get_timing(t))

# Functions
def _plot_graph(x:list,y:list, title:str, chart_type:str):
    chart = chart_type.lower()+'_chart'
    BAR_CHART = dict(
        bar_chart = go.Figure(
            data=[go.Bar(x=x, y=y)],
            layout=dict(title=dict(text=title))
            )
    )
    return BAR_CHART[chart]

def _generate_table(query_result):
    df1 = pd.DataFrame.from_dict({"Number":query_result.keys()})
    df2 = pd.DataFrame.from_dict({"Titles":(query_result.values).tolist()})
    df=pd.concat([df1,df2], axis=1)
    return df.to_dict(orient='records')

def _generate_chart(dict_obj):
    # Create a trace
    trace = go.Scatter(
        y = dict_obj
    )

    data = [trace]

    fig = {
        'data': data
    }
    return fig

# Computations
DATABASE = db.get_data() # fetching all articles from database
# Create forest
forest = Forest(DATABASE)
# Create recommender
recommender = Rengine(DATABASE)



@app.callback([Output('output-table', 'data'),
                Output('output-data-1', 'figure'),
                Output('output-data-2', 'figure')],
              [Input('submit-button', 'n_clicks')],
              [State('input-text', 'value'),
               State('input-recom', 'value'),
               State('input-perm', 'value')])
def update_visualization(n_clicks, text, recommendation, perms):
    # Generates a random sample from a Normal Distribution
    # time_series = np.random.normal(mean, stdv, 1000)
    # # Generates a plotly chart
    # chart_layout = _generate_chart(time_series)
    
    # Get forest
    datab = forest.get_forest(permutations=perms)
    # Making query
    query_result = recommender.make_query(
        text=text, 
        forest=datab,
        permutations=perms,
        num_recommendations=recommendation
        )

    y1 = list(map(CAL, [forest]))
    y2 = list(map(CAL, [recommender]))
    x1 = ["Forest generation"]
    x2 = ["Similarity Search"]
    t1 = lambda s1: "%s seconds"%(s1)
    t2 = lambda s2: "%s miliseconds"%(s2)
    msg1 = "Time: "+print_message(
        (t1(y1[0]),
        "build forest")
        )
    msg2 = "Time: "+print_message(
        (t2(y2[0]*1000),
        "make recommendation(find similar articles)")
        )

    print(msg1, msg2)

    return (
        _generate_table(query_result), 
        _plot_graph(x2, y2, msg2, "Bar"),
        _plot_graph(x1, y1, msg1, "Bar")
        )

@app.callback([Output('output-stats-table', 'columns'),
                Output('output-stats-table', 'data')],
              [Input('submit-button', 'value')])
def update_stats(_):
    stats = db.get_stats()
    df = pd.DataFrame(stats.get('data', None), columns=stats.get('columns', None))
    return [{'name':i, 'id':i} for i in stats.get('columns', None)], df.to_dict(orient='records')
