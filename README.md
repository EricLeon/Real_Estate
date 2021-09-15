# London Flat Analysis

- Built a custom web crawler to automatically download listing information from a popular UK letting website and save it to a local SQLite database.
- Created a data-cleaning pipeline through which I pass freshly scraped data that uniformly parses data into new features that aide in analysis.
- Connect Tableau Desktop to my local database to create dashboards for personal use.


## Framing The Problem

- Objective: Gather and utilise existing data to visualise real estate trends over time in London. I am hoping to identify potentially undervalued flats / areas within the city for further investment analysis.


### Data Collection

I created a custom web crawler to collect this data automatically. I chose to scrape the data from Openrent as it had all of the data points I was interested in. 

The data points I chose to pull off of Openrent were:
[listing title, listing summary, number of beds, number of bathrooms, max occupancy, cost of deposit, rent cost, bills included (Y/N), family friendly (Y/N), pet friendly (Y/N), smoker friendly (Y/N), available from date, minimum tenancy length, garden (Y/N), parking (Y/N), fireplace (Y/N), furnished (Y/N), closest transport station, distance to nearest transport station, property ID, link to the property]

Major challenge(s) overcame:
- Openrent's homepage implements a "lazy-loading" which means that listings only load as the user slowly scrolls down the page. Therefore I decided to use Selenium to automate the process of scrolling down the web page to load all the listings initially. From there I requested the entire web page HTML which I parsed with Beautiful Soup.


![](images/scrape-1.png)
![](images/scrape-2.png)
![](images/scrape-3.png)


## Data Cleaning & Engineering

After scraping the data I needed to clean it up in various ways. The modifications I made to the data were:

- Modified the *available from* date to replace "today" with the date the listing was scraped.
- Parsed the *distance to station* feature and created a new *walk time to station* feature.
- Parsed the *minimum tenancy* feature to take out only the number of months; removing all excess information in this column.
- Removed excess characters from the price fields and changed the data types.
- Created a new feature, *postcode* using the *title* feature. 


## Data Visualisation

For this analysis I created a Tableau Desktop dashboard that would update each time I collected new data. Below are some screenshots of the current version of this dashboard that I use for flat analysis:

* INSERT SCREENSHOTS OF DASHBOARD


## Next Steps

- Create Tableau dashboard
- Finish up README adding in all engineered features and more stuff to top summary
- Incorporate Machine Learning to identify undervalued / over valued properties
- Add to README what I did and ML results / findings. Add more info to top summary
- Set up automatic scraping on Raspberry Pi or similar
- Look into creating a similar scraper / pipeline for houses for sale all over the UK (personal investment)


## Code & Resources Used

- **Python Version:** 3.7
- **Python Libraries:** Selenium, Requests, Beautiful Soup, NumPy, pandas
- **Inspiration:** https://medium.com/geoai/house-hunting-the-data-scientist-way-b32d93f5a42f