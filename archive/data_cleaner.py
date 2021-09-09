import pandas as pd

def CleanListings(raw_data):

    """Cleans and pre-processes data previously scraped from OpenRent.

    It is necessary to call the data_scraper function first and save the
    output to an excel file, as this function looks for an xlsx file
    containing the raw data.

    It goes through column by column parsing various pieces of information
    in order to improve plotting capabilities.

    It will return a DataFrame with the cleaned data.

    Parameters
    ----------
    raw_data : str
        Full path name to existing Excel file containing previously scraped data.

    Returns
    ------
    data : DataFrame
        A Pandas DataFrame containing the cleaned data.
    """

    # Read in raw data
    data = pd.read_excel(raw_data)

    # Fill in available from today to equal the day of scraping
    data.loc[(data['avail_from'] == 'Today'), 'avail_from'] = data['scraped']

    # Convert distance to station into walk time
    data['walk_to_station_mins'] = data['dist_to_station'].apply(lambda x: x.split()[0])

    # Splitting min tenancy term into months only
    data['min_tenancy_months'] = data['min_tenancy'].apply(lambda x: x.split()[0])

    # Cleaning the price columns
    data['deposit'] = data['deposit'].apply(lambda x: float(x.replace('£', '').replace(',', '')))
    data['price'] = data['price'].apply(lambda x: float(x.replace('£', '').replace(',', '')))

    # Parse title column to create 2 new features
    data['postcode'] = data['title'].apply(lambda x: x.split(',')[-1].strip())
    data['area'] = data['title'].apply(lambda x: x.split(',')[-2].strip())

    return data
