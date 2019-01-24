import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

from billboard_web_scraper import top_songs
from spotify_data_append import append_features


##############################################################################
# This script is meant to consolidate all modules of code into one ETL script.
# Step 1: Scrape Billboard for the appropriate endpoints. In this case, all relevant genres I'm looking at.
# Step 2: Read in the CSV generated from web scraping as a DataFrame and get Spotify track IDs, then use those IDs to get song features.
# Step 3: Consolidate the DataFrame with the newly gathered song features by Inner Join on track ID 
# Step 4: Push the merged DataFrame to Postgres.
##############################################################################


def init_tables(genre, endpoint):

    '''
    This function is mainly used to initialize the first few tables in our database.
    Genre and endpoint are going to be fed into a loop to get our first few tables going.
    '''

    # Create connection to database.
    database = "music_data"
    psql_engine = create_engine(f"postgresql://postgres:password@localhost/{database}")

    # Generate CSV for top songs based on genre and endpoint.
    top_songs(genre,endpoint)

    # Plug into Spotify API to fetch song features. Returns merged dataframe.
    df = append_features(genre)

    # Push it to Postgres with table name of the genre we scraped.
    print('Pushing DataFrame to Postgres...') 
    df.to_sql(name=genre,index=False,con=psql_engine,if_exists='replace')
    print(f'Done! {len(df)} rows inserted into table: {genre}.')


def main():
    genre = input("Specify the table name that you'd like to use for this genre: ")
    endpoint = input("Specify the genre's endpoint for Billboard's website that you'd like to scrape: ")

    # Create connection to database.
    database = "music_data"
    psql_engine = create_engine(f"postgresql://postgres:password@localhost/{database}")

    # Generate CSV for top songs based on genre and endpoint.
    top_songs(genre,endpoint)

    # Plug into Spotify API to fetch song features. Returns merged dataframe.
    df = append_features(genre)

    # Push it to Postgres with table name of the genre we scraped.
    print('Pushing DataFrame to Postgres...') 
    df.to_sql(name=genre,index=False,con=psql_engine,if_exists='replace')
    print(f'Done! {len(df)} rows inserted into table: {genre}.')

if __name__=="__main__":
    main()