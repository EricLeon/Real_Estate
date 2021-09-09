from data_scraper import ScrapeFlats
from data_cleaner import CleanListings
import pandas as pd

# Specify paths for data
raw_data_path = 'raw_data.xlsx'
clean_data_path = 'clean_data.xlsx'

# Scrape raw data
raw_data = ScrapeFlats(radius=0, raw_data=raw_data_path)
writer = pd.ExcelWriter(raw_data_path, engine='xlsxwriter')
raw_data.to_excel(writer, index=False)
writer.save()


# Clean raw data
cleaned_data = CleanListings(raw_data=raw_data_path)
writer = pd.ExcelWriter(clean_data_path, engine='xlsxwriter')
cleaned_data.to_excel(writer, index=False)
writer.save()