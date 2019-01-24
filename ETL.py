import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

from billboard_web_scraper import billboard_top_songs
from spotify_data_append import append_features


##############################################################################
# This script is meant to consolidate all modules of data-obtaining code into one ETL script.
# Step 1: Scrape Billboard for the appropriate endpoints. In this case, all relevant genres I'm looking at.
# Step 2: Read in the CSV generated from web scraping as a DataFrame and get Spotify track IDs, then use those IDs to get song features.
# Step 3: Consolidate the DataFrame with the newly gathered song features by Inner Join on track ID 
# Step 4: Push the merged DataFrame to Postgres.
##############################################################################


# Create connection to database.
database = "music_data"
engine = create_engine(f"postgresql://postgres:password@localhost/{database}")


def push_to_sql(df,table_name,engine):
    
    ''' Inserts dataframe rows into SQL table.'''

    # Get dictionaries for each row
    data = df.to_dict(orient='index').values()
    
    # Get column names as one string to pass into SQL statement
    columns = ','.join(df.columns)
    # Format column names to be passed as format strings in SQL statement.
    col_values = ','.join([f':{col}' for col in df.columns])

    with engine.connect() as con:

        statement=text(f"""
            INSERT INTO {table_name} 
            ({columns})
            VALUES
            ({col_values})""")

        for line in data:
            con.execute(statement, **line)
            
            
    print(f"{len(data)} rows inserted into {table_name}.")
    

def init_tables(genre, endpoint):

    '''
    This function is mainly used to initialize the first few tables in our database.
    Genre and endpoint are going to be fed into a loop to get our first few tables going.
    '''

    # Generate CSV for top songs based on genre and endpoint if the CSV doesn't exist already and if there is no backup saved.
    if not os.path.exists(f'top_100_{genre}.csv') and not os.path.exists(f'db_backup/top_100_{genre}_.csv'):
        billboard_top_songs(genre,endpoint)

    
    if not os.path.exists(f'db_backup/top_100_{genre}_.csv'):
        # Plug into Spotify API to fetch song features if backup doesn't exist. Returns merged dataframe.
        df = append_features(genre)
    else:
        # Use backup.
        df = pd.read_csv(f'db_backup/top_100_{genre}_.csv')

    # Create the table.
    with engine.connect() as con:
        print('Dropping table if exists...')
        statement=text(f"""
        DROP TABLE IF EXISTS {genre}
        """)
        con.execute(statement)
        
        print(f'Creating new table: {genre}...')
        statement=text(f"""
        CREATE TABLE {genre} (LIKE hip_hop INCLUDING ALL);
        """)
        con.execute(statement)

    # Push it to Postgres with table name of the genre we scraped.
    print('Pushing DataFrame to Postgres...') 
    push_to_sql(df,genre,engine)



def main():

    '''
    Main function. Biggest difference is this can be used for one-off additions as opposed to a loop in init_tables().
    Genre and endpoint are based off user input.
    '''
    
    genre = input("Specify the table name that you'd like to use for this genre: ")
    endpoint = input("Specify the genre's endpoint for Billboard's website that you'd like to scrape: ")

    # Generate CSV for top songs based on genre and endpoint if the CSV doesn't exist already and if there is no backup saved.
    if not os.path.exists(f'top_100_{genre}.csv') and not os.path.exists(f'db_backup/top_100_{genre}_.csv'):
        billboard_top_songs(genre,endpoint)

    
    if not os.path.exists(f'db_backup/top_100_{genre}_.csv'):
        # Plug into Spotify API to fetch song features if backup doesn't exist. Returns merged dataframe.
        df = append_features(genre)
    else:
        # Use backup.
        df = pd.read_csv(f'db_backup/top_100_{genre}_.csv')

    # Create the table.
    with engine.connect() as con:
        print('Dropping table if exists...')
        statement=text(f"""
        DROP TABLE IF EXISTS {genre}
        """)
        con.execute(statement)
        
        print(f'Creating new table: {genre}...')
        statement=text(f"""
        CREATE TABLE {genre} (LIKE hip_hop INCLUDING ALL);
        """)
        con.execute(statement)

    # Push it to Postgres with table name of the genre we scraped.
    print('Pushing DataFrame to Postgres...') 
    push_to_sql(df,genre,engine)

if __name__=="__main__":
    main()