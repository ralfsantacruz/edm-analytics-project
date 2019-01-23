import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

# Create connection to database.
database = "music_data"
psql_engine = create_engine(f"postgresql://postgres:password@localhost/{database}")


# Read in data
df = pd.read_csv(f"{filename}.csv")

# Push it to Postgres 
df.to_sql(name=name,index=False,con=psql_engine,if_exists='replace')

