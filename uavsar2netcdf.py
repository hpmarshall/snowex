#!/usr/bin/env python3
'''
create ISCE xml metadata file for UAVSAR processed data
https://uavsar.jpl.nasa.gov/cgi-bin/product.pl?jobName=tellur_1701T_17016-005_17018-005_0003d_s01_L090_01#data

Example
uavsar2isce.py -i tellur_1701T_17016-005_17018-005_0003d_s01_L090HH_01.cor.grd -m tellur_1701T_17016-005_17018-005_0003d_s01_L090HH_01.ann

'''
import numpy as np
import argparse
import os
import rasterio


def cmdLineParse():
    '''
    command line arguments
    '''
    parser = argparse.ArgumentParser(description='Create VRT and XML for UAVSAR')
    parser.add_argument('-i','--input', dest='infile', type=str,
            required=True, help='input UAVSAR file (e.g. [name].unw.grd)')
    #parser.add_argument('-o','--output', dest='outfile', type=str,
    #        required=True, help='output vrt file')
    parser.add_argument('-m','--metadata', dest='annfile', type=str,
            required=True, help='associated .ann metadata file')

    return parser.parse_args()


def get_metadata(annfile):
    ''' Read georeference info into dictionary required by rasterio '''
    cmd ="""grep 'Ground Range Data' {} | awk '{{print $8}}' > geodata.txt """.format(annfile)
    os.system(cmd)
    length,width,lat0,lon0,dlat,dlon = np.loadtxt('geodata.txt')
    data = {}
    data['width'] = width
    data['length'] = length
    #data['minx'] = lon0 #center upper left
    #data['miny'] = lat0 #center upper left
    data['deltax'] = dlon
    data['deltay'] = dlat
    #data['maxx'] = lon0 + width*dlon
    #data['maxy'] = lat0 + length*dlat
    #gdal-style geotransform NOTE: might need 0.5,0.5 pixel shift from center to edges
    gt = [lon0, dlon, 0.0, lat0, dlat, 0.0] #0.0 rotationx and y
    print(gt)
    # example from reading landsat data
    data['minx'] = gt[0]
    data['miny'] = gt[3] + data['width'] * gt[4] + data['length']*gt[5]
    data['maxx'] = gt[0] + data['width'] * gt[1] + data['length']*gt[2]
    data['maxy'] = gt[3]

    #data['reference'] = 'WGS84' #for demImage
    return data

#def save_rasterio():
#    ''' '''

# write simple VRT file with info to get into binary files
# use gdal_translate to write as netcdf bands

if __name__ == '__main__':
    inps = cmdLineParse()
    geoinfo = get_metadata(inps.annfile)
    save_rasterio(inps.infile, geoinfo)
