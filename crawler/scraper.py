import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


page = requests.get("https://www.flightera.net/en/airport/Wuhan/ZHHH?mode=departure&OffsetStart=17-Dec-2019_08_50",headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

f = csv.writer(open('WUHAN.csv', 'w'))

x in soup.find_all('td',class_='d-block'):
        #print(link.get_text(strip=True))
        x.append(link.get_text())

x = [item.replace('\n',"") for item in x]

print(x)



# date = ''
# origin = ''
# destination = ''
# departure_time = ''
# arrived_time = ''


# for i in range(len(x)):
#         if (i%1 != 0):
#                 #destination = destination + str(x[i])
#                 print (x[i])

# # print ("dates are ",date)
# # print ("origins are ",origin)
# # print ("destinations are ",destination)
# # print ("departure times are ",departure_time)
# # print ("arrived times are ",arrived_time)



soup = BeautifulSoup(webContent)
a = soup.find('a', href=True, text=re.compile("Next"))
if a:
    link = a["href"]