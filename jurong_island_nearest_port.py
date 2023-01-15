import pandas as pd
from util import get_database_conn, compute_distance

# Create database connection
postgresql_conn = get_database_conn()

def create_jurong_island_nearest_port_table():
    query = 'select * from wpi_data'
    # Get data from database
    wpi_data = pd.read_sql(query, con= postgresql_conn)
    jurong_island_port_cordinates = wpi_data[(wpi_data['Main_port_name']== 'JURONG ISLAND') \
        & (wpi_data['Wpi_country_code'] == 'SG')][['Latitude_degrees', 'Longitude_degrees']]
    jurong_island_port_cordinates = jurong_island_port_cordinates.to_dict('list')
    wpi_data['distance_in_meters'] = wpi_data.apply(lambda x: compute_distance(jurong_island_port_cordinates.get('Latitude_degrees')[0], \
        jurong_island_port_cordinates.get('Longitude_degrees')[0], x['Latitude_degrees'], x['Longitude_degrees']), axis= 1)
    # Sort data by distance in ascending order to get the nearest port distance to jurong_island
    wpi_data_sorted = wpi_data.sort_values(by=['distance_in_meters'], ascending= True)
    jurong_island_nearest_ports = wpi_data_sorted[['Main_port_name', 'distance_in_meters']].head()
    # Write data to postgresql database
    jurong_island_nearest_ports.to_sql('jurong_island_nearest_ports', con= postgresql_conn, if_exists='replace')
    print('jurong_island_nearest_ports data successfully written to table in the database')

create_jurong_island_nearest_port_table()