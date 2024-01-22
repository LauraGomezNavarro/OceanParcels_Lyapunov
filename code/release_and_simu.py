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

####################
# Parameters:

#Particle_AZO_grid100000_notides_Dec_week01_hourly.nc
grid_name = "1-64grid"
nyear = 2019
nmonth = 10
simu_length = 15. # monthly # days

# Defining grid of starting particles:

if grid_name == "1-8grid":
    step = .125 # degrees
elif grid_name == "1-64grid":
    step = 0.015625 # 1./64degrees
else:
    print("Error")
    fszfasgasg
    
lons, lats = np.meshgrid(np.arange(360.-30, 360.-15+step, step), np.arange(32, 38+step, step))
lons.shape[0]*lons.shape[1]

data_path = '../validation/'
fname = 'datos_Laura.nc'

outdir = '../examples/'

# Define start date:
start_day = 1 #[1, 8, 15, 22]

outname = outdir + "Particle_AZO_fFTLE_" + grid_name + "_" + str(nmonth).zfill(2) + str(start_day).zfill(2) + "_" + str(simu_length)[0:2] + "d"
####################

####################
# Parcels simulation
pset = ParticleSet(fieldset=fieldset, pclass=JITParticle, lon=lons, lat=lats, time=datetime(nyear, nmonth, start_day, 0, 0)) #30))

output_file = pset.ParticleFile(name=outname, outputdt=timedelta(hours=6))

#minutes=6*60
pset.execute(AdvectionRK4, runtime=timedelta(days=simu_length), dt=timedelta(hours=6),
      output_file=output_file) #recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle},

output_file.export()  # export the trajectory data to a netcdf file
####################
