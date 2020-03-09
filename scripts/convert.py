import csv
import datetime
from time import gmtime, strftime
from datetime import timedelta
import urllib.request
import pandas
import json
import geojson
import pandas as pd
import geopandas as gpd



#list of countries



#gettting Data from current date. This is the daily report

def getcsv():
    global curr_date
    curr_date = datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime("%m-%d-%Y")
    u = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+ curr_date + ".csv"
    urllib.request.urlretrieve (u, "scripts/data_latest.csv")
    #print(curr_date)
    #print(u)


getcsv()

# open and get data from csv file

csvfile = pandas.read_csv('scripts/data_latest.csv', encoding='utf-8')
csvfile.columns = csvfile.columns.str.strip().str.lower().str.replace('/', '_').str.replace('(', '').str.replace(')', '')

#for i in range(len(csvfile)):
#    if(csvfile.country_region[i] not in Countries) :
#        print(csvfile.country_region[i])




pd.set_option('display.max_columns', 300)
fname = ('/home/anton/Desktop/COVID19/scripts/world.geojson')
df = gpd.read_file(fname)


df["deaths"] = 0
df["confirmed"] = 0




# Combining all CHINA and USA

#China
total_confirmed_china = 0
total_death_china = 0
china_count = 0
for i in csvfile.country_region:
    if(i == "Mainland China"):
        #print(csvfile.iloc[china_count]['confirmed'])
        total_confirmed_china = csvfile.iloc[china_count]['confirmed'] + total_confirmed_china
        total_death_china = csvfile.iloc[china_count]['deaths'] + total_death_china
    china_count += 1
print(total_confirmed_china)
print(total_death_china)



#USA
total_confirmed_usa = 0
total_death_usa = 0
usa_count = 0
for i in csvfile.country_region:
    if(i == "US"):
        #print(csvfile.iloc[china_count]['confirmed'])
        total_confirmed_usa = csvfile.iloc[usa_count]['confirmed'] + total_confirmed_usa
        total_death_usa = csvfile.iloc[usa_count]['deaths'] + total_death_usa
    usa_count += 1
print(total_confirmed_usa)
print(total_death_usa)


#Add China and USA total to CSVfile tally

for i in range(len(df.name)):
    if((df.name[i] == "USA")):
        df.at[i,'deaths'] = total_death_usa
    elif ((df.name[i] == "China")):
        df.at[i,'deaths'] = total_death_china

for i in range(len(df.name)):        
    if ((df.name[i] == "China")):
        df.at[i,'confirmed'] = total_confirmed_china
    elif ((df.name[i] == "USA")):
        df.at[i,'confirmed'] = total_confirmed_usa




#########################################

count = 0
for i in csvfile.country_region:
     for j in range(len(df.name)):
             if ( (i == df.name[j]) and (csvfile.iloc[count]['deaths'] != 0) ):
                     #print(i,df.name[j])
                     # Add df.death value
                     df.at[j,'deaths'] = csvfile.iloc[count]['deaths']



     count = count + 1



count1 = 0
for i in csvfile.country_region:
     for j in range(len(df.name)):
             if ( (i == df.name[j]) and (csvfile.iloc[count1]['confirmed'] != 0) ):
                     #print(i,df.name[j])
                     # Add df.death value
                     df.at[j,'confirmed'] = csvfile.iloc[count1]['confirmed']


     count1 = count1 + 1



#wriing

with open('test1.json','w') as f:
    f.write(df.to_json())

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(df)