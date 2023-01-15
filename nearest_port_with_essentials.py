import pandas as pd
from util import get_database_conn, compute_distance

# Create database connection
postgresql_conn = get_database_conn()

def create_nearest_port_with_essentials_table():
    '''
    This function creates a table containing the nearest ports with essentials 
    (provision, provision, water, fuel_oil and diesel) in the postgresql database
    instance.

    Parameter: Doest to accept any parameter
    Return value: None
    Return type: None
    '''
    query = '''
    select "Wpi_country_code" country, "Main_port_name" port_name, "Latitude_degrees" port_latitude, "Longitude_degrees" port_longitude
    from wpi_data
    where "Supplies_provisions" = 'Y' and "Supplies_water" = 'Y' and "Supplies_fuel_oil" = 'Y'
    and "Supplies_diesel_oil" = 'Y'
    '''
    # Get the data of ports with provision, water, fuel_oil and diesel from database
    ports_with_essentials = pd.read_sql(query, con= postgresql_conn)
    caller_coordinates = {'latitude':32.610982, 'longitude':-38.706256}
    ports_with_essentials['port_distance_meters'] = ports_with_essentials.apply(lambda x: compute_distance(caller_coordinates.get('latitude'), \
        caller_coordinates.get('longitude'), x['port_latitude'], x['port_longitude']), axis= 1)
    # Sort data by port_distance_meters in ascending order to get the shortest distance port distance to caller
    ports_with_essentials_sorted = ports_with_essentials.sort_values(by=['port_distance_meters'], ascending= True)
    nearest_port = ports_with_essentials_sorted[['country', 'port_name', 'port_latitude', 'port_longitude']].head(1)
    # Write data to postgresql database
    nearest_port.to_sql('nearest_port_with_essentials', con= postgresql_conn, if_exists='replace')
    print('nearest_port_with_essentials data successfully written to table in the database')

create_nearest_port_with_essentials_table()