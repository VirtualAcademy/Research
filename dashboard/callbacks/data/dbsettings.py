import os


DATABASE_SETTINGS = {
    "DPATH": os.path.dirname(__file__),
    "DNAME": "database",
    "QUERRY": lambda x:"SELECT * FROM %s;"%(x),
    "STATS": {
        "columns":['Table', 'Total Rows', 'Total Columns'],# 'Columns'],
        "data":{
            'Table':['authors','paper_authors' ,'papers'],
            'Total Rows': [8653 ,18321, 6560],
            'Total Columns': [2, 3, 7],
            # 'Columns': [
            #     ["id, name"],
            #     ["id, paper_id, author_id"],
            #     ["id, year, title, event_type, pdf_name, abstract, paper_text"]]
            }
        }
    }

def get_path():
    return os.path.join(DATABASE_SETTINGS["DPATH"], DATABASE_SETTINGS["DNAME"]+".sqlite")