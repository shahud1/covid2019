import requests
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup


base_url = 'https://nh.craigslist.org/d/computer-parts/search/syp'
base_search_url = 'https://nh.craigslist.org'
urls = []
urls.append(base_url)
dates = []
titles = []
prices = []
hoods = []

while len(urls) > 0: # while we have urls to crawl
    print(urls)
    url = urls.pop(0) # removes the first element from the list of urls
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    next_url = soup.find('a', class_= "button pagenum") # finds the next urls to crawl
    if next_url: # if it's not an empty string
        urls.append(base_search_url + next_url['href']) # adds next url to crawl to the list of urls to crawl

    listings = soup.find_all('li', class_= "result-row") # get all current url listings
    # this is your code unchanged
    for listing in listings:
        datar = listing.find('time', {'class': ["result-date"]}).text
        dates.append(datar)

        title = listing.find('a', {'class': ["result-title"]}).text
        titles.append(title)

        try:
            price = listing.find('span', {'class': "result-price"}).text
            prices.append(price)
        except:
            prices.append('missing')

        try:
            hood = listing.find('span', {'class': "result-hood"}).text
            hoods.append(hood)
        except:
            hoods.append('missing')

#write the lists to a dataframe
listings_df = pd.DataFrame({'Date': dates, 'Titles' : titles, 'Price' : prices, 'Location' : hoods})

 #write to a file
listings_df.to_csv("craigslist_listings.csv")