# import needed libraries
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values
dotenv_values()


def get_database_conn():
    # Get database credentials from environment variable
    config = dict(dotenv_values('.env'))
    db_user = config.get('DB_USER')
    db_password = config.get('DB_PASSWORD')
    db_name = config.get('DB_NAME')
    port = config.get('PORT')
    host = config.get('HOST')
    # Create connection to Postgresql database
    return create_engine(f'postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}')

# Create a connection to the Microsoft Access database file
access_db_engine = create_engine("access+pyodbc://@wpi_data")

wpi_data_tables = ['WPI Region', 'WPI Import', 'Wpi Data', 'Shelter Afforded LUT', 'Repairs Code LUT', 'Maximum Size Vessel LUT', \
'Harbor Type LUT', 'Harbor Size LUT', 'Drydock/Marine Railway Code LUT', 'Depth Code LUT', 'Country Codes', 'Country Codes Old']

# Function to load data from access database to postgresql database
def load_data_to_db():
    '''
    Function to load data to database
    '''
    postgres_engine = get_database_conn()
    for table_name in wpi_data_tables:
        table_data = pd.read_sql(table_name, access_db_engine)
        # Generate valid table names for destination tables in postgresql
        destination_table_name = '_'.join(table_name.lower().split(' '))
        table_data.to_sql(destination_table_name, con= postgres_engine, if_exists='replace')
    print('Data successfully successfully loaded to posgresql database')


# def create_table_relationships():
#     connection = get_database_conn().raw_connection()
#     cursor = connection.cursor()
#     query = '''
#     ALTER TABLE country_codes_old ADD CONSTRAINT country_code_unique UNIQUE ("Country Code");
#     ALTER TABLE wpi_data ADD FOREIGN KEY ("Wpi_country_code") REFERENCES country_codes_old ("Country Code");
#     '''
#     cursor.execute(query)
    
    
# create_table_relationships()
