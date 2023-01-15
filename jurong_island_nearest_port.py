import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from etl import get_database_conn

# Create database connection
postgresql_conn = get_database_conn()

def compute_port_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    '''
    A helper function for computing the distance between two points using their
    latitude and longitude coordinates.
    Parameters: This function takes the latitude and longitude coordinate values of
    the two points as parameters
    
    Return value: returns a float value of the calculated distance in meters
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

query = 'select * from wpi_data'
# Get data from database
wpi_data = pd.read_sql(query, con= postgresql_conn)
jurong_island_port_cordinates = wpi_data[(wpi_data['Main_port_name']== 'JURONG ISLAND') \
    & (wpi_data['Wpi_country_code'] == 'SG')][['Latitude_degrees', 'Longitude_degrees']]
jurong_island_port_cordinates = jurong_island_port_cordinates.to_dict('list')
wpi_data['distance_in_meters'] = wpi_data.apply(lambda x: compute_port_distance(jurong_island_port_cordinates.get('Latitude_degrees')[0], \
    jurong_island_port_cordinates.get('Longitude_degrees')[0], x['Latitude_degrees'], x['Longitude_degrees']), axis= 1)
# Sort data in ascending order
wpi_data.sort_values(by=['distance_in_meters'], ascending= True)
jurong_island_nearest_ports = wpi_data[['Main_port_name', 'distance_in_meters']].head()
# Write data to postgresql database
jurong_island_nearest_ports.to_sql('jurong_island_nearest_ports', con= postgresql_conn, if_exists='replace')
print('jurong_island_nearest_ports data successfully written to database')

