#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 22:42:43 2017

@author: hpm
"""


import pandas as pd
import glob
import numpy as np
#import psycopg2

def readSnowpit(filename):
    #filename='Pit_Output/2017-02-06/PIT_L36/pit_20170206_L36.xlsx'
    print(filename)
    xl = pd.ExcelFile(filename)
    data=pd.read_excel(xl,sheetname=0,parse_cols='H')
    UTMN=int(data['UTMN:'][0])
    UTME=int(data['UTMN:'][2])
    UTMzone=data['UTMN:'][4]
    density=pd.read_excel(xl,sheetname=0,header=8,parse_cols='E:F')
    # mean_density=density.dropna().mean().mean()
    mean_density=density.dropna().mean().mean()
    np.where(np.abs(mean_density)>=1000,np.nan,mean_density)
    data=pd.read_excel(xl,sheetname=0,header=0,parse_cols='F')
    depth=float(data['Total Depth (cm)'][0])
    data=pd.read_excel(xl,sheetname=0,header=0,parse_cols='M')
    pit_date=data['Surveyors:'][2]
    data=pd.read_excel(xl,sheetname=0,header=0,parse_cols='O')
    pit_time=data['Time:'][0]
    SWE=depth*mean_density/1000
    r=pd.DataFrame(columns={'UTM_N','UTM_E','UTM_zone','date','time','depth','density','SWE'})
    r.set_value(0,'UTM_N',UTMN)
    r.set_value(0,'UTM_E',UTME)
    r.set_value(0,'UTM_zone',UTMzone)
    r.set_value(0,'date',pit_date)
    r.set_value(0,'time',pit_time)
    r.set_value(0,'depth',depth)
    r.set_value(0,'density',mean_density)
    r.set_value(0,'SWE',SWE)
    return r

pits=pd.DataFrame(columns={'UTM_N','UTM_E','UTM_zone','date','time','depth','density','SWE'})
for filename in glob.iglob('./Pit_output/**/*.xlsx',recursive=True): # loop over all GPS files
    r=readSnowpit(filename)
    pits=pits.append(r,'ignore_index=True') # append to pits data frame the current pit

import json
import sqlalchemy
with open("postgres.json") as f:
    db_conn_dict = json.load(f)
cred_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_conn_dict)
dbeng = sqlalchemy.create_engine(cred_string)
pits.to_sql('SnowEx_snowpits', dbeng)