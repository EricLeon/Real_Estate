# IMPORTS
import pandas as pd
from selenium import webdriver
from time import sleep
import random
import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3

# FUNCTIONS
def scrape_flats(database_path, radius=2):

	"""
	Scrapes Open Rent for flat listings in London, UK with a user-provided radius.

	This function utilises a headless selenium instance to scroll to the bottom of the web-page before requesting the HTML in BeautifulSoup. This is because Open Rent uses lazy loading, and not all listings are shown when the web-page is loaded. The user needs to scroll all the way to the bottom to view all of the search results.

	Parameters
	----------
	radius : int -> Default = 2
		Radius around London in which to expand the search.
	
	existing_ids : list
		The existing property ID's in the database

	Returns
	------
	data : DataFrame
		DataFrame containing all relevant information on scraped flats.
	"""

	# Create variables for feedback
	num_scraped = 0
	today = datetime.date.today().strftime("%d %B %Y")

	# Check existing listings to avoid dupes
	try:
		existing_ids = get_existing_properties(database_path)
	except sqlite3.OperationalError:
		existing_ids = []

	# Request web page and simulate scrolling to bottom (Lazy Loading)
	link = f'https://www.openrent.co.uk/properties-to-rent/london?term=London&area={radius}'
	driver = webdriver.Safari()
	driver.get(link)
	sleep(random.randint(4,7))

	lastHeight = driver.execute_script("return document.body.scrollHeight")
	pause = 1
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(pause)
		newHeight = driver.execute_script("return document.body.scrollHeight")
		if newHeight == lastHeight:
			break
		lastHeight = newHeight

	# Request entire web page source in BeautifulSoup to parse and close browser
	sleep(random.randint(2,4))
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	driver.close()

	# Create lists to hold data
	property_link_list, property_id_list, title_list, description_list, location_list = ([] for i in range(5))
	bedrooms_list, bathrooms_list, max_tenants_list, deposit_list, rent_list = ([] for i in range(5))
	bills_included_list, student_list, family_list, pet_list, smoker_list = ([] for i in range(5))
	avail_from_list, min_tenancy_list, garden_list, parking_list, fireplace_list = ([] for i in range(5))
	furnishing_list, all_stations_list, closest_station_list, postcode_list = ([] for i in range(4))

	# Scrape each listing
	listings = soup.find_all(attrs={'class': 'pli clearfix'})

	for listing in listings:
		property_link = 'https://www.openrent.co.uk/' + listing['href']
		property_id = property_link.split('/')[-1]

		# Visit detailed listings; only if not previously scraped
		if int(property_id) in existing_ids:
			pass

		else:
			sub_soup = BeautifulSoup(requests.get(property_link).text, 'html.parser')
			
			try:
				title = sub_soup.find(attrs={'class': 'property-title'}).get_text().strip()
				postcode = title.split(',')[-1].strip()
			except:
				title = None
				postcode = None

			try:
				description = sub_soup.find(attrs={'class': 'description'}).get_text().strip()
			except:
				description = None

			# Overview Table
			try:
				table = sub_soup.find(attrs={'class': 'table table-striped intro-stats'})
				rows = table.find_all('td')
				location = rows[1].get_text().strip()
				bedrooms = int(rows[3].get_text().strip())
				bathrooms = int(rows[5].get_text().strip())
				max_tenants = int(rows[7].get_text().strip())
			except:
				location = 'London'
				bedrooms = -1
				bathrooms = -1
				max_tenants = -1

			# Price & Bills
			try:
				table = sub_soup.find_all(attrs={'class': 'table table-striped'})[0]
				rows = table.find_all('td')
				deposit = int(rows[1].get_text().strip().replace('£', '').replace(',','').split('.')[0])
				rent_pcm = int(rows[3].get_text().strip().replace('£', '').replace(',','').split('.')[0])
				bills_included = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'
			except:
				deposit = -1
				rent_pcm = -1
				bills_included = 'Undefined'

			# Tenant Preferences
			try:
				table = sub_soup.find_all(attrs={'class': 'table table-striped'})[1]
				rows = table.find_all('td')
				student_friendly = 'Yes' if rows[1].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				family_friendly = 'Yes' if rows[3].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				pet_friendly = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				smoker_friendly = 'Yes' if rows[7].find('i').attrs['class'][-1] == 'fa-check' else 'No'
			except:
				student_friendly = 'Undefined'
				family_friendly = 'Undefined'
				pet_friendly = 'Undefined'
				smoker_friendly = 'Undefined'

			# Availability
			try:
				table = sub_soup.find_all(attrs={'class': 'table table-striped'})[2]
				rows = table.find_all('td')
				available = rows[1].get_text().strip()
				avail_from = today if available == 'Today' else available
				min_tenancy = int(rows[3].get_text().split()[0])
			except:
				available = 'Undefined'
				min_tenancy = -1


			# Features
			try:
				table = sub_soup.find_all(attrs={'class': 'table table-striped'})[3]
				rows = table.find_all('td')
				garden = 'Yes' if rows[1].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				parking = 'Yes' if rows[3].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				fireplace = 'Yes' if rows[5].find('i').attrs['class'][-1] == 'fa-check' else 'No'
				furnishing = rows[7].get_text().strip()
			except:
				garden = 'Undefined'
				parking = 'Undefined'
				fireplace = 'Undefined'
				furnishing = 'Undefined'

			# Transportation
			try:
				table = sub_soup.find(attrs={'class': 'table table-striped mt-1'})
				data_rows = table.find_all('td')[4:]
				stations = data_rows[::3]
				all_stations = [x.get_text().strip() for x in stations]
				distances = data_rows[1::3]
				closest_station_mins = int(distances[0].get_text().strip().split()[0])
			except:
				all_stations = ['Undefined']
				closest_station_mins = -1

			property_id_list.append(property_id)
			property_link_list.append(property_link)
			title_list.append(title)
			description_list.append(description)
			location_list.append(location)
			bedrooms_list.append(bedrooms)
			bathrooms_list.append(bathrooms)
			max_tenants_list.append(max_tenants)
			deposit_list.append(deposit)
			rent_list.append(rent_pcm)
			bills_included_list.append(bills_included)
			student_list.append(student_friendly)
			family_list.append(family_friendly)
			pet_list.append(pet_friendly)
			smoker_list.append(smoker_friendly)
			avail_from_list.append(avail_from)
			min_tenancy_list.append(min_tenancy)
			garden_list.append(garden)
			parking_list.append(parking)
			fireplace_list.append(fireplace)
			furnishing_list.append(furnishing)
			all_stations_list.append(all_stations)
			closest_station_list.append(closest_station_mins)
			postcode_list.append(postcode)

			# Print feedback
			num_scraped += 1
			print(f"{num_scraped} new listings scraped")
			sleep(random.random() * 1.1)

	# Create DataFrame
	data_dict = {
		'property_id':property_id_list, 'property_link':property_link_list, 'listing_title':title_list,
		'description':description_list, 'location':location_list, 'num_bedrooms':bedrooms_list,
		'num_bathrooms':bathrooms_list, 'max_tenants':max_tenants_list, 'deposit':deposit_list,
		'rent_pcm':rent_list, 'bills_included':bills_included_list, 'student_friendly':student_list,
		'family_friendly':family_list, 'pet_friendly':pet_list, 'smoker_friendly':smoker_list,
		'available_from':avail_from_list, 'min_tenancy_months':min_tenancy_list, 'garden':garden_list,
		'parking':parking_list, 'fireplace':fireplace_list, 'furnishing':furnishing_list,
		'nearby_stations':all_stations_list, 'closest_station_mins':closest_station_list, 
		'postcode':postcode_list}
	
	data = pd.DataFrame(data_dict)
	data['scrape_date'] = today
	return data


def populate_database(data, database_path):
	"""
	Dumps data scraped from Openrent into database in current working directory.

	Parameters
	----------
	data : dataframe
		Data scraped from Openrent. Typically using the scrape_flats function.
	
	database_path : str
		The path to the database where this data is stored. If in CWD then this is just the database name.

	Returns
	------
	"""

	conn = sqlite3.connect(database_path)
	data.to_sql('rentals', conn, if_exists='append', index=False, dtype={
		'property_id':'text', 'property_link':'text', 'listing_title':'text', 'description':'text',
		'location':'text', 'num_bedrooms':'integer', 'num_bathrooms':'integer', 'max_tenants':'integer', 
		'deposit':'real', 'rent_pcm':'real', 'bills_included':'integer', 'student_friendly':'integer', 
		'family_friendly':'integer', 'pet_friendly':'integer', 'smoker_friendly':'integer', 
		'available_from':'text', 'min_tenancy_months':'integer', 'garden':'integer', 'parking':'integer',
		'fireplace':'integer', 'furnishing':'text', 'nearby_stations':'text', 
		'closest_station_mins':'integer', 'postcode':'text', 'scrape_date':'text'
		})


def get_existing_properties(database_path):
	"""
	Gets the existing property ID's from the database to avoid scraping duplicate listings.

	Parameters
	----------
	database_path : str
		The path to the database where this data is stored. If in CWD then this is just the database name.

	Returns
	------
	ids : list
		List of the existing propery_id's in the database.
	"""

	conn = sqlite3.connect(database_path)
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	ids = c.execute('SELECT property_id FROM rentals').fetchall()
	return ids




