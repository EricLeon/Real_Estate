# ~~~~~~~~~~ IMPORTS ~~~~~~~~~~ #
from selenium import webdriver
from time import sleep
import random
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd


def ScrapeFlats(raw_data, radius=2):

    """Scrapes OpenRent for flat listings in London, UK.

    It's important that an Excel file with all the column names is already
    created and that the exact path to this file is specifie as an argument
    for this function.

    When called this function will read in any existing data, load a headless
    instance of Safari and scroll to the bottom of the results page. This is
    because of the dynamic (lazy) loading that is used; before requesting the
    webpage source to parse in BeautifulSoup, we need to actually load all the
    listings on one page.

    It will return a DataFrame with the newly scraped data appended to any
    existing data.

    Parameters
    ----------
    raw_data : str
        Full path name to existing Excel file containing previously scraped data.

    radius : int, default=2
        Radius surrounding Central London at which to cap flat search.

    Returns
    ------
    housing_data : DataFrame
        A Pandas DataFrame containing all previous data concatenated with all new listings.
    """

    # ~~~~~~~~~~ READ IN EXISTING DATA ~~~~~~~~~~ #
    existing_data = pd.read_excel(raw_data)
    existing_props = set(pd.Series(existing_data['property_id']))
    print(f'{len(existing_data)} listings already in database. Searching for new ones...\n')


    # ~~~~~~~~~~ LAZY SCROLLING THE ENTIRE WEB PAGE ~~~~~~~~~~ #
    link = f'https://www.openrent.co.uk/properties-to-rent/london?term=London&area={radius}'
    driver = webdriver.Safari()
    driver.get(link)
    sleep(5)

    # Simulate scrolling to bottom of webpage
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    pause = 0.5
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(pause)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    # Request entire web page source
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()

    # ~~~~~~~~~~ SCRAPING EACH LISTING ~~~~~~~~~~ #

    # Create lists to hold data
    title_list, summary_list, bed_list, bath_list, max_occupancy_list, deposit_list = ([] for i in range(6))
    rent_list, bills_inc_list, students_list, families_list, pets_list, smokers_list = ([] for i in range(6))
    avail_from_list, min_tenancy_list, garden_list, parking_list, fireplace_list, furnishing_list = ([] for i in range(6))
    station_list, station_dist_list, prop_id_list, direct_link_list = ([] for i in range(4))


    # Scrape each listing
    listings = soup.find_all(attrs={'class': 'pli clearfix'})
    num_scraped = 0

    for listing in listings:
        sub_link = 'https://www.openrent.co.uk/' + listing['href']
        prop_id = sub_link.split('/')[-1]

        # Only scrape properties I don't have already
        if int(prop_id) in existing_props:
            continue

        else:
            try:
                title = listing.find(attrs={'class': 'banda pt listing-title'}).get_text().strip()
            except:
                title = ''

            try:
                summary = listing.find(attrs={'class': 'listing-desc'}).get_text().strip()
            except:
                summary = ''

            # Simulate visiting each listing
            sub_soup = BeautifulSoup(requests.get(sub_link).text, 'html.parser')

            # Summary stats -> Find table, return all rows in array form
            table = sub_soup.find(attrs={'class': 'table table-striped intro-stats'})
            rows = table.find_all('td')
            beds = rows[3].get_text().strip()
            baths = rows[5].get_text().strip()
            max_occupancy = rows[7].get_text().strip()

            # Price and bills -> Find table, return all rows in array form
            table = sub_soup.find_all(attrs={'class': 'table table-striped'})[0]
            rows = table.find_all('td')
            deposit = rows[1].get_text().strip()
            rent = rows[3].get_text().strip()
            bills_inc = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'

            # Tenant Preference - > Find table, return all rows in array form
            table = sub_soup.find_all(attrs={'class': 'table table-striped'})[1]
            rows = table.find_all('td')
            students = 'Yes' if rows[1].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            families = 'Yes' if rows[3].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            pets = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            smokers = 'Yes' if rows[7].find('i').attrs['class'][-1] == 'fa-check' else 'No'

            # Availability - > Find table, return all rows in array form
            table = sub_soup.find_all(attrs={'class': 'table table-striped'})[2]
            rows = table.find_all('td')
            avail_from = rows[1].get_text().strip()
            min_tenancy = rows[3].get_text().strip()

            # Features - > Find table, return all rows in array form
            table = sub_soup.find_all(attrs={'class': 'table table-striped'})[3]
            rows = table.find_all('td')
            garden = 'Yes' if rows[1].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            parking = 'Yes' if rows[3].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            fireplace = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'
            furnishing = rows[7].get_text().strip()

            # Transportation -> Find table, return all rows in array form
            table = sub_soup.find(attrs={'class': 'table table-striped mt-1'})
            rows = table.find_all('td')
            station = rows[4].get_text().strip()
            station_dist = rows[5].get_text().strip()

            # Append data to each list
            title_list.append(title)
            summary_list.append(summary)
            bed_list.append(beds)
            bath_list.append(baths)
            max_occupancy_list.append(max_occupancy)
            deposit_list.append(deposit)
            rent_list.append(rent)
            bills_inc_list.append(bills_inc)
            students_list.append(students)
            families_list.append(families)
            pets_list.append(pets)
            smokers_list.append(smokers)
            avail_from_list.append(avail_from)
            min_tenancy_list.append(min_tenancy)
            garden_list.append(garden)
            parking_list.append(parking)
            fireplace_list.append(fireplace)
            furnishing_list.append(furnishing)
            station_list.append(station)
            station_dist_list.append(station_dist)
            prop_id_list.append(prop_id)
            direct_link_list.append(sub_link)

            # Print feedback
            num_scraped += 1
            print(f"{num_scraped} listings scraped")
            sleep(random.random() * 1.1)

    # Create DataFrame
    data_dict = {"title": title_list, "summary": summary_list, "beds": bed_list, "baths": bath_list,
                 "max_tenants": max_occupancy_list, "deposit": deposit_list, "price":rent_list,
                 "bills_included": bills_inc_list, "student_friendly":students_list, "family_friendly":families_list,
                 "pet_friendly":pets_list, "smoker_friendly":smokers_list, "avail_from":avail_from_list,
                 "min_tenancy":min_tenancy_list, "garden":garden_list, "parking":parking_list,
                 "fireplace":fireplace_list, "furnishing":furnishing_list, "closest_station":station_list,
                 "dist_to_station":station_dist_list, "property_id":prop_id_list, 'link':direct_link_list}
    new_data = pd.DataFrame(data_dict)

    # Add scrape date
    today = datetime.date.today().strftime("%Y-%m-%d")
    new_data["scraped"] = today

    # Print feedback
    print(f"Scraping completed - {len(new_data)} listings found!")

    # Concat new data to old data
    housing_data = pd.concat([existing_data, new_data])
    print(f'There are now {len(housing_data)} listings in the database.')
    return housing_data





