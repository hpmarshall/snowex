#!/bin/bash

export ARIACONF=/home/scott/.aria2/asf.conf
#export START='2017-01-01T00:00:00UTC'
#export END='2017-02-28T23:59:59UTC'
export COLLECTION='tellur'
export PLATFORM='UAVSAR'
export POLYGON="POLYGON((-108.63+37.63,-108.05+37.65,-107.45+37.68,-107.55+39.21,-108.64+39.21,-108.63+37.63))"
export PROCLEVEL='INTERFEROMETRY_GRD'

# NOTE: polygon is redundant with 'collection name'

# CSV
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=csv > asf_uavsar.csv 

# KML
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=kml > asf_uavsar.kml

# GeoJSON
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=json > asf_uavsar.json 

# Metalink (to actually download)
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=metalink > asf_uavsar.metalink

#aria2c --http-auth-challenge=true --conf-path=$ARIACONF asf_uavsar.metalink 
