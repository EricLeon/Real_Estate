
from data_utils import scrape_flats, populate_database, get_existing_properties
import pandas as pd

# data = scrape_flats(radius = 5, database_path = 'real_estate.db')
# data.to_csv('scraped_data.csv', index=False)
data = pd.read_csv('scraped_data.csv')
populate_database(data = data, database_path = 'real_estate.db')