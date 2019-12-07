import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

layout_stats = html.Div([
    html.H3("DataSet Statistics:"),
    html.P(
        """This dataset includes the title, authors, abstracts, and extracted text for all NIPS
        papers to date (ranging from the first 1987 conference to the current 2016 conference). The paper text was extracted from the raw PDF files and are released both in CSV files and as a SQLite database. The code 
        to scrape and create this dataset is on GitHub: https://github.com/benhamner/nips-papers)"""),
    html.Div([
    dt.DataTable(
        id='output-stats-table',
        style_as_list_view=True,
        style_cell={'textAlign': 'center','width':'30%'}
        )], style={'width':'50%','margin':'auto'})
    ], className='row center')