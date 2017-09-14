# Download UAVSAR SNOWEX data and convert to netCDF

All the snowex UAVSAR data is stored at Alaska Satellite Facility. The bash scripts in this folder will download all the data from ASF and the `uavsar2netcdf.py` will convert the format:

*be sure to modify asf.conf with your NASA login credentials*

```
./download_uavsar_interferograms.sh
unzip tellur_1701T_17016-005_17018-005_0003d_s01_L090_01_int_grd.zip 
./uavsar2netcdf.py tellur_1701T_17016-005_17018-005_0003d_s01_L090HH_01.cor.grd
```

