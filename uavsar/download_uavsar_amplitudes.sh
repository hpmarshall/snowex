#!/bin/bash

export ARIACONF=./asf.conf
export COLLECTION='tellur'
export PLATFORM='UAVSAR'
export POLYGON="POLYGON((-108.63+37.63,-108.05+37.65,-107.45+37.68,-107.55+39.21,-108.64+39.21,-108.63+37.63))"
export PROCLEVEL='AMPLITUDE_GRD'

# CSV
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&processingLevel=$PROCLEVEL\&output=csv > asf_uavsar_amplitudes.csv 

# KML
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=kml > asf_uavsar_amplitudes.kml

# GeoJSON
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=json > asf_uavsar_amplitudes.json 

# Metalink (to actually download)
curl https://api.daac.asf.alaska.edu/services/search/param?collectionName=$COLLECTION\&intersectsWith=$POLYGON\&platform=$PLATFORM\&relativeOrbit=$FRAME\&processingLevel=$PROCLEVEL\&output=metalink > asf_uavsar_amplitudes.metalink

aria2c --http-auth-challenge=true --conf-path=$ARIACONF asf_uavsar_amplitudes.metalink 
