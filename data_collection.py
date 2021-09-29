
from data_utils import scrape_flats, populate_database, get_existing_properties
import pandas as pd
from joblib import load

# Import pre-fit transformation pipeline and tuned ML model
pipeline = load('full_pipeline.joblib')
model = load('tuned_model.joblib')

# Scrape data and populate database
scrape_flats(transformation_pipeline = pipeline, model = model, radius = 5, database_path = 'real_estate.db')
populate_database(database_path = 'real_estate.db')