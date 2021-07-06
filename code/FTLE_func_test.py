from math import sin, cos, sqrt, atan2, radians
import numpy as np
import xarray as xr
import numpy.linalg as LA

def dist_pairs_km(inlon1, inlon2, inlat1, inlat2):
    """
    Haversine formula used, which assumes the Earth is a sphere.
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


filedir = '/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/wtides/monthly/' #ntides

ds = xr.open_dataset(filedir + 'Particle_AZO_grid100000p_wtides_0601_hourly_MONTH.nc') #ntides

step = .04 # degrees
grid_lons, grid_lats = np.meshgrid(np.arange(-35, -18+step, step), np.arange(30, 40+step, step))

x0 = np.reshape(ds['lon'][:,0].data, ( grid_lons.shape[0], grid_lons.shape[1] ))
x1 = np.reshape(ds['lon'][:,-1].data,( grid_lons.shape[0], grid_lons.shape[1] ))
y0 = np.reshape(ds['lat'][:,0].data, ( grid_lons.shape[0], grid_lons.shape[1] )) 
y1 = np.reshape(ds['lat'][:,-1].data, ( grid_lons.shape[0], grid_lons.shape[1] ))


H = x0.shape[0] 
L = x0.shape[1]

FTLE_f = np.ones_like(x0) * np.nan

Td = 30. # days

J = np.empty([2,2],float)

# 1, H-1 --> to ignore bordersx for now
for i in range(1, H-1): # 0, H-2
    for j in range(1, L-1): # 0, L-2
        J[0][0] = dist_pairs_km(x1[i,j],x1[i-1,j], y1[i,j],y1[i-1,j]) / dist_pairs_km(x0[i,j],x0[i-1,j], y0[i,j],y0[i-1,j])
        ##gradF[:,0,0] = (X1rav[x1p] - X1rav[x1m])/dx1
        J[0][1] = dist_pairs_km(x1[i,j],x1[i,j-1], y1[i,j],y1[i,j-1]) / dist_pairs_km(x0[i,j],x0[i,j-1], y0[i,j],y0[i,j-1])
        J[1][0] = dist_pairs_km(x1[i,j],x1[i,j+1], y1[i,j],y1[i,j+1]) / dist_pairs_km(x0[i,j],x0[i,j+1], y0[i,j],y0[i,j+1])
        J[1][1] = dist_pairs_km(x1[i,j],x1[i+1,j], y1[i,j],y1[i+1,j]) / dist_pairs_km(x0[i,j],x0[i+1,j], y0[i,j],y0[i+1,j])
        
        if np.isnan(J).any():
            continue  
        else:
       
            D = np.dot(np.transpose(J),J)
            ##-->same
            # its largest eigenvalue
            lamda = LA.eigvals(D)
            ##-->same
            lam_max = max(lamda)
            FTLE_f[i][j] = (1/Td) * np.log(np.sqrt(lam_max))
            ##-->from sinha paper and from https://github.com/anirban89/llc_offline_lagrangian_analysis/blob/master/plot_lagrangian_diagnostics.ipynb

savedir = '/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/FTLE/'
savename = savedir + 'FTLE_wtides_0601.npz' #'KDE_' + nfile.split('/')[-1].split('.nc')[0] + '.npz'
np.savez(savename, FTLE_f=FTLE_f) 

