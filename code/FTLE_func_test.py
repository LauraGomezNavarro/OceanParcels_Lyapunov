from math import sin, cos, sqrt, atan2, radians
import numpy as np
import xarray as xr
import numpy.linalg as LA

def dist_pairs(inx1, inx2, iny1, iny2, coords):
    """
    
    """
    if coords = 'km':
    # Euclidean distance calculated.
    # source: https://www.delftstack.com/howto/numpy/calculate-euclidean-distance/#use-the-distance.euclidean-function-to-find-the-euclidean-distance-between-two-points

        a = np.array((inx1, iny1))
        b = np.array((inx2, iny2))

        distance = np.sqrt(np.sum(np.square(a - b)))

    elif coords = 'degrees':
    #Haversine formula used, which assumes the Earth is a sphere.
    #source: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    
        # approximate radius of earth in km
        R = 6373.0

        lon1 = radians(inx1)
        lat1 = radians(iny1)
        lon2 = radians(inx2)
        lat2 = radians(iny2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
    else:
        print('Missing coords. param.')
        sdhskdhg
        
    return distance

def FTLE(filename, Td, step, domain, coords, savename):
    """
    filename: input path and filename, for example, filename = '/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/wtides/monthly/' + 'Particle_AZO_grid100000p_wtides_0601_hourly_MONTH.nc'
    
    Td: Simualtion length in days, for example 30. # days
    
    step: initial separation of particles (in degrees).  Both in longitude and latitude. Example: step = .04 # degrees
    
    domain: [minimum lon, maximum lon, minimum lat, maximum lat]; longitude in degrees East and latitude in degrees north. Example = [-35, -18, 30, 40]
    
    coords: Indicates the units of the coordinates of the input variables: 
    - 'degrees'
    - 'km'
    
    savename: output path and filename, for example, savename = savedir + 'FTLE_wtides_0601.npz' 
    
    """
    # Checking if file is netcdf or zarr and opening with zarray open_dataset accordingly
    if filename.split('.')[-1][0:2] == 'nc':
        ds = xr.open_dataset(filename)
    elif filename.split('.')[-1][0:2] == 'za':
        ds = xr.open_dataset(filename, engine="zarr")
        ds = ds.compute() # so that it goes faster and it does not have to go to each zarr file folder
    else: 
        print('File type or name error')
        dsgjsdhkgh

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
            J[0][0] = dist_pairs(x1[i,j],x1[i-1,j], y1[i,j],y1[i-1,j]) / dist_pairs(x0[i,j],x0[i-1,j], y0[i,j],y0[i-1,j])
            ##gradF[:,0,0] = (X1rav[x1p] - X1rav[x1m])/dx1
            J[0][1] = dist_pairs(x1[i,j],x1[i,j-1], y1[i,j],y1[i,j-1]) / dist_pairs(x0[i,j],x0[i,j-1], y0[i,j],y0[i,j-1])
            J[1][0] = dist_pairs(x1[i,j],x1[i,j+1], y1[i,j],y1[i,j+1]) / dist_pairs(x0[i,j],x0[i,j+1], y0[i,j],y0[i,j+1])
            J[1][1] = dist_pairs(x1[i,j],x1[i+1,j], y1[i,j],y1[i+1,j]) / dist_pairs(x0[i,j],x0[i+1,j], y0[i,j],y0[i+1,j])

            if np.isnan(J).any():
                continue  
            else:

                D = np.dot(np.transpose(J),J)
                # its largest eigenvalue:
                lamda = LA.eigvals(D)
                lam_max = max(lamda)
                FTLE_x[i][j] = (1/Td) * np.log(np.sqrt(lam_max))
                
    np.savez(savename, FTLE=FTLE_x) 

