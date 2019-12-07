
####################################################################################################################
# About this Dataset
# (https://www.kaggle.com/benhamner/exploring-the-nips-papers)
# Neural Information Processing Systems (NIPS) is one of the top machine learning conferences in the world. It covers
# topics ranging from deep learning and computer vision to cognitive science and reinforcement learning.

# This dataset includes the title, authors, abstracts, and extracted text for all NIPS papers to date (ranging from
# the first 1987 conference to the current 2016 conference). I've extracted the paper text from the raw PDF files and
# are releasing that both in CSV files and as a SQLite database. The code to scrape and create this dataset is on 
# GitHub: https://github.com/benhamner/nips-papers
##################################################################################################################

import pandas as pd
import sqlite3
from callbacks.data.dbsettings import DATABASE_SETTINGS, get_path

def get_data():
    db_path = get_path()
    conn = sqlite3.connect(db_path)
    query = DATABASE_SETTINGS["QUERRY"]('papers')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_stats():
    return DATABASE_SETTINGS.get('STATS', None)
