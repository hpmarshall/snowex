#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:45:44 2017

@author: hpm
"""

import pandas as pd
import sqlalchemy
import json

with open("postgres.json") as f:
    db_conn_dict = json.load(f)

#Create secrete string!
cred_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_conn_dict)

# create our SQL engine
dbeng = sqlalchemy.create_engine(cred_string)

# BELOW CODE WROTE CSV FILE TO A TABLE IN THE SQL DATABASE
#url="https://raw.githubusercontent.com/hpmarshall/snowex/master/Pit_Output/snowex_pit_out.csv"
#csv_file = pd.read_csv(url) 
#csv_file.to_sql('SnowExPits', dbeng)

# BELOW CODE DOESN"T WORK>>>SOMETHING WRONG WITH ALTER statement
# now lets change these utm coordinates to lat/lon, or find the WGS UTM code for Colorado
#dbnamePts = 'SnowExPits'
#dbeng.execute("""ALTER TABLE %s ADD COLUMN geom geometry(Point, 4326);""" %(dbnamePts)) 
## populate the geometry field
#dbeng.execute("""UPDATE %s SET geom = ST_Transform(ST_setSRID(ST_MakePoint(x_utm13n,y_utm13n),32613),4326);""" %(dbnamePts))

# LETS READ IN SnowExPits table and plot
data=pd.read_sql_table('SnowExPits',dbeng)
 # figure out how to make this DataFrame into a GeoDataFrame
import geopandas as gpd
dataXY=pd.DataFrame(data,columns=['x_utm13n','y_utm13n']) # grab just X/Y from data frame
from shapely.geometry import Point
geometry = [Point(xy) for xy in zip(dataXY['x_utm13n'], dataXY['y_utm13n'])]
dataGeo=gpd.GeoDataFrame(dataXY,geometry=geometry) # convert to geopandas
dataGeo.crs = {'init': 'epsg:32613'}
# ok now try transforming into lat/lon:
dataGeoLatLon=dataGeo.to_crs(epsg=4326)
# plot first for Grand Mesa study area
#fig, ax1 = plt.subplots()


# lets read in the basin boundary shape file
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()
SBBboundary=gpd.read_file('SenatorBeckBasinBoundary/poly.shp')
SBBboundaryLatLon=SBBboundary.to_crs(epsg=4326)

SBBboundaryLatLon.plot(ax=ax1)
#ax1=dataGeoLatLon.plot(color='red')
ax1.set_ylim(37.885,37.925)
ax1.set_xlim(-107.74,-107.705)

# Equivalent
#ax1.plot(dataGeoLatLon.lon,  dataGeoLatLon.lat, 'ko')
dataGeoLatLon.plot(ax=ax1, color='k')


#ax1.set_ylim(38.97,39.15)
#ax1.set_xlim(-108.25,-107.85)
# Now for Senator Beck Study Site
#ax1=dataGeoLatLon.plot()
ax1.set_ylim(37.885,37.925)
ax1.set_xlim(-107.74,-107.705)


plt.show()