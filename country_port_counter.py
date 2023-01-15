import pandas as pd
from util import get_database_conn

# Create database connection
postgresql_conn = get_database_conn()

def create_country_port_count_table():
    '''
    The function retrieves the data countries and their number of port with a Cargo_wharf
    and creates a table for the resulting data in a postgresql database.
    parameters: It takes no parameter
    Return value: Does not return a value.
    '''
    query = '''
    select  "Wpi_country_code" country, count("Main_port_name") port_count
    from wpi_data
    where "Load_offload_wharves" = 'Y'
    group by 1
    order by count("Main_port_name") desc
    limit 1
    '''
    country_port_count_data = pd.read_sql(query, con= postgresql_conn)
    # Write country_port_count_data to postgresql database
    country_port_count_data.to_sql('country_port_count', con= postgresql_conn, if_exists='replace')
    print('country_port_count_data successfully written to a table in the database')

if __name__== '__main__':
    create_country_port_count_table()