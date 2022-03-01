from math import sqrt, dist
import numpy as np
import xarray as xr
import numpy.linalg as LA

def dist_metric_pairs(inx1, inx2, iny1, iny2):
    """
    Euclidean distance calculated.
    source: https://www.delftstack.com/howto/numpy/calculate-euclidean-distance/#use-the-distance.euclidean-function-to-find-the-euclidean-distance-between-two-points
    """
    a = np.array((inx1, iny1))
    b = np.array((inx2, iny2))

    distance = np.sqrt(np.sum(np.square(a - b)))

    return distance

def FTLE(filename, Td, step, domain, savename):
    """
    filename: example '/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/wtides/monthly/' + 'Particle_AZO_grid100000p_wtides_0601_hourly_MONTH.nc'
    Td = Simualtion length in days, for example 30. # days
    step = initial separation of particles (in degrees).  Both in logitude and latitude. Example: step = .04 # degrees
    domain = [minimum lon, maximum lon, minimum lat, maximum lat]; longitude in degrees East and latitude in degrees north. Example = [-35, -18, 30, 40]
    savename = example savename = savedir + 'FTLE_wtides_0601.npz' #'KDE_' + nfile.split('/')[-1].split('.nc')[0] + '.npz' ; savedir = '/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/FTLE/'
    
    """

    ds = xr.open_dataset(filename)

    grid_lons, grid_lats = np.meshgrid(np.arange(domain[0], domain[1]+step, step), np.arange(domain[2], domain[3]+step, step))

    x0 = np.reshape(ds['lon'][:,0].data, ( grid_lons.shape[0], grid_lons.shape[1] ))
    x1 = np.reshape(ds['lon'][:,-1].data,( grid_lons.shape[0], grid_lons.shape[1] ))
    y0 = np.reshape(ds['lat'][:,0].data, ( grid_lons.shape[0], grid_lons.shape[1] )) 
    y1 = np.reshape(ds['lat'][:,-1].data, ( grid_lons.shape[0], grid_lons.shape[1] ))


    H = x0.shape[0] 
    L = x0.shape[1]

    FTLE_x = np.ones_like(x0) * np.nan

    J = np.empty([2,2],float)

    # 1, H-1 --> to ignore bordersx for now
    for i in range(1, H-1): # 0, H-2
        for j in range(1, L-1): # 0, L-2
            J[0][0] = dist_metric_pairs(x1[i,j],x1[i-1,j], y1[i,j],y1[i-1,j]) / dist_metric_pairs(x0[i,j],x0[i-1,j], y0[i,j],y0[i-1,j])
            ##gradF[:,0,0] = (X1rav[x1p] - X1rav[x1m])/dx1
            J[0][1] = dist_metric_pairs(x1[i,j],x1[i,j-1], y1[i,j],y1[i,j-1]) / dist_metric_pairs(x0[i,j],x0[i,j-1], y0[i,j],y0[i,j-1])
            J[1][0] = dist_metric_pairs(x1[i,j],x1[i,j+1], y1[i,j],y1[i,j+1]) / dist_metric_pairs(x0[i,j],x0[i,j+1], y0[i,j],y0[i,j+1])
            J[1][1] = dist_metric_pairs(x1[i,j],x1[i+1,j], y1[i,j],y1[i+1,j]) / dist_metric_pairs(x0[i,j],x0[i+1,j], y0[i,j],y0[i+1,j])

            if np.isnan(J).any():
                continue  
            else:

                D = np.dot(np.transpose(J),J)
                # its largest eigenvalue:
                lamda = LA.eigvals(D)
                lam_max = max(lamda)
                FTLE_x[i][j] = (1/Td) * np.log(np.sqrt(lam_max))
                
    np.savez(savename, FTLE=FTLE_x) 
