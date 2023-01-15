# import needed libraries
import pandas as pd
from sqlalchemy import create_engine
from util import get_database_conn
import urllib.request
import zipfile

def download_data():
    '''
    This function downloads the required data for this assessment in a zip file and extracts it into the
    directory named data withing the project directory.
    Parameter: Does not accept any parameter
    Return value: None
    Return type: None
    '''
    url = 'https://msi.nga.mil/api/publications/download?key=16694622/SFH00000/PUB150.ZIP'
    file_name = url.split("/")[-1]
    urllib.request.urlretrieve(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall('data')
    print("File successfully downloaded and extracted to the directory 'data'.")

# Create a connection to the Microsoft Access database file
access_db_engine = create_engine("access+pyodbc://@wpi_data")
wpi_data_tables = ['WPI Region', 'WPI Import', 'Wpi Data', 'Shelter Afforded LUT', 'Repairs Code LUT', 'Maximum Size Vessel LUT', \
'Harbor Type LUT', 'Harbor Size LUT', 'Drydock/Marine Railway Code LUT', 'Depth Code LUT', 'Country Codes', 'Country Codes Old']

# Function to load data from access database to postgresql database
def load_data_to_db():
    '''
    This function establish connection to the Microsoft access database file and loads each table
    in the database to a postgresql database instance.

    Parameter: Does not accept a parameter
    Return value: Does not return a value. It performs a write operation to the database
    Return type: None
    '''
    postgres_engine = get_database_conn()
    for table_name in wpi_data_tables:
        table_data = pd.read_sql(table_name, access_db_engine)
        # Generate valid table names for destination tables in postgresql
        destination_table_name = '_'.join(table_name.lower().split(' '))
        table_data.to_sql(destination_table_name, con= postgres_engine, if_exists='replace')
    print('Data successfully successfully loaded to posgresql database')

