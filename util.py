from math import sin, cos, sqrt, atan2, radians
from sqlalchemy import create_engine
from dotenv import dotenv_values
dotenv_values()

def get_database_conn():
    '''
    This function retrieve database credentials from environment variable file (.env)
    and create a connection object used for establishing connection to a postgresql
    database instance.
    Parameter: Does not accept a parameter
    Return value: return a postgresql database connection object
    Return type: database obeject
    '''
    # Get database credentials from environment variable
    config = dict(dotenv_values('.env'))
    db_user_name = config.get('DB_USER_NAME')
    db_password = config.get('DB_PASSWORD')
    db_name = config.get('DB_NAME')
    port = config.get('PORT')
    host = config.get('HOST')
    # Create and return a postgresql database connection object
    return create_engine(f'postgresql+psycopg2://{db_user_name}:{db_password}@{host}:{port}/{db_name}')

def compute_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    '''
    A helper function for computing the distance between two points using their
    latitude and longitude coordinates.
    
    Parameters: This function takes the latitude and longitude coordinate values of
    the two points as parameters
    Return value: the distance between two ports in meters
    Return type: Returns a float value.
    '''
    # approximate radius of earth in meters
    earth_radius = 6373000
    # latitude and longitude were converted from degress to radians
    longitude_distance = radians(longitude_2 - longitude_1)
    latitude_distance = radians(latitude_2 - latitude_1)
    # We use the haversine formular to calculate the distance between two points on the earth
    a = abs(sin(latitude_distance/2)**2 + cos(latitude_1) * cos(latitude_2) * sin(longitude_distance /2)**2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c