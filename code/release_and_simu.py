from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4
from datetime import timedelta, datetime
from glob import glob
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter#
import matplotlib.ticker as mticker

def release_and_simu(grid_name, datetime_in, simu_length, domain, filename, outname):
    """
    grid_name: e.g. "1-64grid"
    datetime_in: e.g. datetime(2019, 10, 1, 0, 0)
    simu_length: in days e.g. 15.
    domain: spatial domain of particle release e.g. domain = [360.-12, 360.-8, 32., 36.] #lomin, lomax, lamin, lamax
    filename: e.g. '../validation/' + 'datos_Laura.nc'
    outname: e.g. '../examples/' + "Particle_AZO_fFTLE_" + grid_name + "_" + str(nmonth).zfill(2) + str(start_day).zfill(2) + "_" + str(simu_length)[0:2] + "d"
    """
    ####################
    # Defining grid of starting particles:
    if grid_name == "1-8grid":
        step = .125 # degrees
    elif grid_name == "1-64grid":
        step = 0.015625 # 1./64degrees
    else:
        print("Error")
        fszfasgasg

    lons, lats = np.meshgrid(np.arange(domain[0], domain[1]+step, step), np.arange(domain[2], domain[3]+step, step))
    ####################
    
    ####################
    # Parcels simulation
    
    variables = {'U': 'ugos', 'V': 'vgos'}

    filenames = {'U': filename, 'V': filename}

    dimensions = {'U': {'lat': 'latitude', 'lon': 'longitude', 'time': 'time'},
                  'V': {'lat': 'latitude', 'lon': 'longitude', 'time': 'time'}}

    fieldset = FieldSet.from_netcdf(filenames, variables, dimensions)

    
    pset = ParticleSet(fieldset=fieldset, pclass=JITParticle, lon=lons, lat=lats, time=datetime_in) #30))

    output_file = pset.ParticleFile(name=outname, outputdt=timedelta(hours=6))

    #minutes=6*60
    pset.execute(AdvectionRK4, runtime=timedelta(days=simu_length), dt=timedelta(hours=6),
          output_file=output_file) #recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle},

    output_file.export()  # export the trajectory data to a netcdf file
    
    ####################
