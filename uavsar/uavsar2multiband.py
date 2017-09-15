#!/usr/bin/env python3
'''
create ISCE xml metadata file for UAVSAR processed data
https://uavsar.jpl.nasa.gov/cgi-bin/product.pl?jobName=tellur_1701T_17016-005_17018-005_0003d_s01_L090_01#data

NOTE: pass just basename of int and amp zip files

Example:
uavsar2multiband.py -i tellur_1701T_17016


Output: Multiband netCDF with following bands: 
[unw, hgt, amp1, amp2, coh]
[unwrapped phase, dem elevation, amplitude1, amplitude2, coherence]
'''
import numpy as np
import argparse
import os
import re


def cmdLineParse():
    '''
    command line arguments
    '''
    parser = argparse.ArgumentParser(description='Create VRT and XML for UAVSAR')
    parser.add_argument('-i','--input', dest='infile', type=str,
            required=True, help='input UAVSAR file (e.g. [name]_int_grd.zip)')
    
    return parser.parse_args()


def get_metadata(infile):
    ''' read georeference metadata into python dictionary '''
    annfile = infile.split('.')[0] + '.ann'

    with open(annfile) as ann:
        lines = ann.readlines()

    geolines = [l for l in lines if l.startswith('Ground Range Data')]
    numbers = re.compile(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+")
    
    strings = [numbers.findall(x)[0] for x in geolines]
    #floats = [float(x) for x in strings]
    length,width,lat0,lon0,dlat,dlon = strings
    
    meta = {}
    meta['GeoTransform'] = ', '.join([lon0, dlon, '0.0', lat0, '0.0', dlat])
    meta['rasterXSize'] = int(width)
    meta['rasterYSize'] = int(length)
    meta['dataType'] = 'Float32'
    meta['LineOffset'] = meta['rasterXSize']*4
    meta['SourceFilename'] = infile 

    return meta


def write_VRT(infile, metadata):
    ''' simple metadata file so that binary files are recognized by GDAL'''
    with open(infile + '.vrt', 'w') as vrt:
        vrt.write('''
<VRTDataset rasterXSize="{rasterXSize}" rasterYSize="{rasterYSize}">
    <SRS>EPSG:4326</SRS>
    <GeoTransform>{GeoTransform}</GeoTransform>
    <VRTRasterBand band="1" dataType="{dataType}" subClass="VRTRawRasterBand">
        <SourceFilename relativeToVRT="1">{SourceFilename}</SourceFilename>
        <ByteOrder>LSB</ByteOrder>
        <ImageOffset>0</ImageOffset>
        <PixelOffset>4</PixelOffset>
        <LineOffset>{LineOffset}</LineOffset>
    </VRTRasterBand>
</VRTDataset>
'''.format(**metadata))


def unzip(zipfile):
    '''quick system call to unzip a file '''
    os.system('unzip {}'format(zipfile))


def convert_to_multiband_netCDF(infile):
    ''' use gdal_translate to write as netcdf bands '''
    # NOTE: not sure about naming bands or including metadata...
    cmd = 'gdal_merge.py -o {}.nc -of netCDF -separate *vrt'.format(infile)
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    inps = cmdLineParse()
    zipfiles = glob.glob(inps.infile + '*.zip')
    [unzip(z) for z in zipfiles] #NOTE: could remove these to save space afterwards
    allbands = glob.glob('tellur_1701T_17016-005_17018-005*grd')
    basename = allbands[0].split('.')[0]

    extensions = ['amp1.grd', 'amp2.grd', 'cor.grd', 'hgt.grd', 'unw.grd']
    bands = [basename + ext for ext in extensions] 

    # Metadata is same for all these files (common grid)
    meta = get_metadata(zipfiles[0]))
    
    for b in bands:
        write_VRT(inps.infile, meta)
    
    convert_to_netCDF(inps.infile)
    
    print('Done!')

