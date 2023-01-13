# import needed libraries
import pandas as pd
from sqlalchemy import create_engine
import os

data_path = f'{os.getcwd()}/data'
# Create a connection to the Microsoft Access database file
engine = create_engine("access+pyodbc://@wpi_data")
wpi_data = pd.read_sql('WPI', engine)
print(wpi_data.head())
