import pandas as pd
import sqlalchemy
import json
import requests
from bs4 import BeautifulSoup

def get_snow_links():
    """ Get all URL links """
    
    # create response object
    r = requests.get(archive_url)
     
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html5lib')
     
    # find all links on web-page
    links = soup.findAll('a')
 
    # filter the link sending with .mp4
    video_links = [link['href'] for link in links if link['href'].endswith('csv')]
    
    # Retunr to user
    return video_links

# Open postgress server file
with open("postgres.json") as f:
    db_conn_dict = json.load(f)

#Create secrete string!
cred_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_conn_dict)

# create our SQL engine
dbeng = sqlalchemy.create_engine(cred_string)

# raw URL
raw_url = "https://raw.githubusercontent.com/hpmarshall/snowex/master/RadarGPS/"

# specify the URL of the archive here
archive_url = "https://github.com/hpmarshall/snowex/tree/master/RadarGPS"

# Get all links 
links = get_snow_links()

# Loop trough links
for link in links:
    
    # Converte from unicide to string    
    link_name = link.encode('ascii','ignore')
    
    # get index of last "/"
    i = link_name.rfind('/') + 1
    
    # Create download URL
    url = raw_url + link_name[i:]

    # Read the file into pandas
    csv_file = pd.read_csv(url) 
    
    # Push to SQL server
    csv_file[0:10].to_sql(link_name[i:], dbeng)
