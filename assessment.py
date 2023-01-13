# import needed libraries
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values
dotenv_values()
import os

# Get database credentials from environment variable
config = dict(dotenv_values('.env'))
db_user = config.get('DB_USER')
db_password = config.get('DB_PASSWORD')
db_name = config.get('DB_NAME')
port = config.get('PORT')

# Create a connection to the Microsoft Access database file
access_db_engine = create_engine("access+pyodbc://@wpi_data")
# Create connection to Postgresql database
postgres_engine = create_engine(f'postgresql://{db_user}:{db_password}@localhost:{port}/{db_name}')

wpi_data_tables = ['WPI Region', 'WPI Import', 'Wpi Data', 'Shelter Afforded LUT', 'Repairs Code LUT', 'Maximum Size Vessel LUT', \
'Harbor Type LUT', 'Harbor Size LUT', 'Drydock/Marine Railway Code LUT', 'Depth Code LUT', 'Country Codes', 'Country Codes Old']

# Function to load data from access database to postgresql database
def load_data_to_db():
    for table_name in wpi_data_tables:
        table_data = pd.read_sql(table_name, access_db_engine)
        # Generate valid table names for destination tables in postgresql
        destination_table_name = '_'.join(table_name.lower().split(' '))
        table_data.to_sql(destination_table_name, con= postgres_engine, if_exists='replace')
    print('Data successfully loaded to posgresql database')


#load_data_to_db()