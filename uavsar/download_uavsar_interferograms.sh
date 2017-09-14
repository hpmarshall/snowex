#!/bin/bash

export ARIACONF=./asf.conf
export PLATFORM='UAVSAR'
export POLYGON="POLYGON((-108.63+37.63,-108.05+37.65,-107.45+37.68,-107.55+39.21,-108.64+39.21,-108.63+37.63))"
export PROCLEVEL='PROJECTED'

# Sentinel-1A
curl https://api.daac.asf.alaska.edu/services/search/param?\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=csv > asf_uavsar.csv 

curl https://api.daac.asf.alaska.edu/services/search/param?\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=kml > asf_uavsar.kml

curl https://api.daac.asf.alaska.edu/services/search/param?\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=json > asf_uavsar.json 

curl https://api.daac.asf.alaska.edu/services/search/param?\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=metalink > asf_uavsar.metalink

aria2c --http-auth-challenge=true --conf-path=$ARIACONF asf_uavsar.metalink
