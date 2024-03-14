#from gemini : /nethome/gomez023/parcels_Azores/eNATL60/FTLE/FS_b_Jan_wtides_biw_w01_v02_upd02.py
from datetime import timedelta, datetime
from glob import glob
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from collections import namedtuple
from shapely import geometry

from math import sin, cos, sqrt, atan2, radians
import numpy as np
import xarray as xr
import numpy.linalg as LA

# Adapted from test03, adding the sqrt in FTLE calcn after discussing with Darshika (this version should be up to date w/ github function!!!
# reorganized filename and savename so easier to modify!!!

def dist_pairs_km(inlon1, inlon2, inlat1, inlat2):
    """
    source: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    
    """
    # approximate radius of earth in km
    R = 6373.0

    lon1 = radians(inlon1)
    lat1 = radians(inlat1)
    lon2 = radians(inlon2)
    lat2 = radians(inlat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

from scipy.spatial import distance

step = .004 # degrees
grid_lons, grid_lats = np.meshgrid(np.arange(-27, -21+step, step), np.arange(32.5, 36.5+step, step))

filedir_root = "/data/oceanparcels/output_data/data_LauraGN/Lorenz_outputs/"

ds_wT_Jan =  xr.open_dataset(filedir_root + 'Particle_AZO_grid_wtides_0101_biweekly_hourly_BACK_v02.nc')

nmonth = 'Jan'
ds = ds_wT_Jan

t_filename = 'wT'

savename = 'FS_b_' + t_filename + '_' + nmonth + '_biw_w01_v02' + '_upd02.npz'

lons_mesh = np.reshape(ds['lon'][:,:].data, ( grid_lons.shape[0], grid_lons.shape[1], 337))
lats_mesh = np.reshape(ds['lat'][:,:].data, ( grid_lons.shape[0], grid_lons.shape[1], 337))

print("start =", datetime.now().time())

H = lons_mesh.shape[0]
L = lons_mesh.shape[1]

FS_b = np.ones_like(lats_mesh[:,:,0]) * np.nan

J = np.empty([2,2],float) * np.nan

# 1, H-1 --> to ignore bordersx for now
for i in range(1, H-1): # 0, H-2
    for j in range(1, L-1): # 0, L-2

        aa = list(zip(lats_mesh[i,j,:], lons_mesh[i,j,:]))
        bb1 = list(zip(lats_mesh[i+1,j,:], lons_mesh[i+1,j,:]))
        bb2 = list(zip(lats_mesh[i-1,j,:], lons_mesh[i-1,j,:]))
        bb3 = list(zip(lats_mesh[i,j+1,:], lons_mesh[i,j+1,:]))
        bb4 = list(zip(lats_mesh[i,j-1,:], lons_mesh[i,j-1,:]))

        dist_pairs1=[]
        dist_pairs2=[]
        dist_pairs3=[]
        dist_pairs4=[]
        for ii in range(0, len(aa)):
            dd1 = dist_pairs_km(aa[ii][1], bb1[ii][1], aa[ii][0], bb1[ii][0])
            dist_pairs1.append(dd1)
            dd2 = dist_pairs_km(aa[ii][1], bb2[ii][1], aa[ii][0], bb2[ii][0])
            dist_pairs2.append(dd2)
            dd3 = dist_pairs_km(aa[ii][1], bb3[ii][1], aa[ii][0], bb3[ii][0])
            dist_pairs3.append(dd3)
            dd4 = dist_pairs_km(aa[ii][1], bb4[ii][1], aa[ii][0], bb4[ii][0])
            dist_pairs4.append(dd4)

        ind_pairs1 = next((x[0] for x in enumerate(dist_pairs1) if x[1] > (dist_pairs1[0] * np.sqrt(2))), np.nan)
        if np.isnan(ind_pairs1) :
            J[0][0] = np.nan
        else:
            difft1 = (ds['time'][0,0].data - ds['time'][0,ind_pairs1].data)
            J[0][0] = difft1 / np.timedelta64(1, 'D')

        ind_pairs2 = next((x[0] for x in enumerate(dist_pairs2) if x[1] > (dist_pairs2[0] * np.sqrt(2))), np.nan)
        if np.isnan(ind_pairs2) :
            J[0][1] = np.nan
        else:
            difft2 = (ds['time'][0,0].data - ds['time'][0,ind_pairs2].data)
            J[0][1] = difft2 / np.timedelta64(1, 'D')

        ind_pairs3 = next((x[0] for x in enumerate(dist_pairs3) if x[1] > (dist_pairs3[0] * np.sqrt(2))), np.nan)
        if np.isnan(ind_pairs3) :
            J[1][0] = np.nan
        else:
            difft3 = (ds['time'][0,0].data - ds['time'][0,ind_pairs3].data)
            J[1][0] = difft3 / np.timedelta64(1, 'D')

        ind_pairs4 = next((x[0] for x in enumerate(dist_pairs4) if x[1] > (dist_pairs4[0] * np.sqrt(2))), np.nan)
        if np.isnan(ind_pairs4) :
            J[1][1] = np.nan
        else:
            difft4 = (ds['time'][0,0].data - ds['time'][0,ind_pairs4].data)
            J[1][1] = difft4 / np.timedelta64(1, 'D')

        TJ = np.nanmin(J)

        FS_b[i][j] = (1/TJ) * np.log(np.sqrt(2))

        print("end =", datetime.now().time())

np.savez(savename, FS_b=FS_b)

print("end =", datetime.now().time())
                                      