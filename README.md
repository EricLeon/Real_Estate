# London Flat Analysis

- Built a custom web crawler to automatically download listing information from a popular UK letting website and ran it every day for a month.
- Created a data-cleaning pipeline through which I pass freshly scraped data that uniformly parses data into new features that aide in analysis.
- Produced a Tableau dashboard which I personally use frequently in my own search for the perfect London flat to let.


## Framing The Problem

- Objective: Gather and utilise existing data to visualise real estate trends over time in London.
- Why: I was looking for a tool that would allow me to analyse certain aspects of a property as I searched for a new property to rent. When I couldn't find one that met exactly what I was looking for, I decided to create my own.



### Data Collection

I created a custom web crawler to collect this data automatically. I chose to scrape the data from Openrent as it had all of the data points I was interested in. Currently I run this script to scrape and clean the data manually however in the future would like to explore setting it up using a Raspberry Pi or some other automated system.

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
- Created 2 new features *postcode* and *area* using the *title* feature. 


## Data Visualisation

For this analysis I wanted to create a living Tableau dashboard that would be updated each time I ran the web crawler to include all new information. The dashboard can be found and downloaded [on my Tableau Public profile](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)



## In Action

[![Check out the dashboard](images/dash1.png)](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)
[![Check out the dashboard](images/dash2.png)](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)
[![Check out the dashboard](images/dash3.png)](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)
[![Check out the dashboard](images/dash4.png)](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)
[![Check out the dashboard](images/dash5.png)](https://public.tableau.com/profile/eric.leon#!/vizhome/LondonFlatAnalysisWIP/FlatOverview)


## Code & Resources Used
- **Python Version:** 3.7
- **Python Libraries:** Selenium, Requests, Beautiful Soup, NumPy, pandas
