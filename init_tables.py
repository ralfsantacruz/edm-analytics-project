from ETL import init_tables

#### ONLY RUN SCRIPT IF YOU HAVE MORE THAN ONE GENRE. ####

def main():

    # table_names = ['pop', 'country', 'rock','latin']
    # endpoints = ['pop-songs', 'hot-country-songs', 'hot-rock-songs','hot-latin-songs']
    table_names = []
    endpoints = []

    if table_names and endpoints and len(table_names)==len(endpoints):
        for genre, endpoint in zip(table_names, endpoints):
            init_tables(genre,endpoint)
    else:
        print("There were no arguments to pass into the initialization function, or you provided lists of unequal length.")

if __name__=="__main__":
    main()