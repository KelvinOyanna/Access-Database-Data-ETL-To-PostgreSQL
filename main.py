from jurong_island_nearest_port import create_jurong_island_nearest_port_table
from country_port_counter import create_country_port_count_table
from nearest_port_with_essentials import create_nearest_port_with_essentials_table
from etl import download_data, load_data_to_db

def main():
    # Download the required data from the web
    download_data()
    # Load data from the Microsoft access database file to a postgresql database
    load_data_to_db()
    # Create tables in the database with data from the result of the questions asked
    create_jurong_island_nearest_port_table()
    create_country_port_count_table()
    create_nearest_port_with_essentials_table()

main()
