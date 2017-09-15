#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:45:44 2017

@author: hpm
"""

import pandas as pd
import sqlalchemy
import json
import requests
from bs4 import BeautifulSoup

with open("postgres.json") as f:
    db_conn_dict = json.load(f)

#Create secrete string!
cred_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_conn_dict)

# create our SQL engine
dbeng = sqlalchemy.create_engine(cred_string)
url="https://raw.githubusercontent.com/hpmarshall/snowex/master/Pit_Output/snowex_pit_out.csv"
csv_file = pd.read_csv(url) 
csv_file.to_sql('SnowExPits', dbeng)