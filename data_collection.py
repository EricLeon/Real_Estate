
from data_utils import scrape_flats, populate_database, get_existing_properties
import pandas as pd

scrape_flats(radius = 5, database_path = 'real_estate.db')
populate_database(database_path = 'real_estate.db')