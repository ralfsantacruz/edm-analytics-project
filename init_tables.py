from ETL import init_tables

def main():

    table_names = []
    endpoints = []

    if table_names and endpoints:
        for genre, endpoint in zip(table_names, endpoints):
            init_tables(genre,endpoint)
    else:
        print("There were no arguments to pass into the initialization function.")