from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4
from datetime import timedelta, datetime
import numpy as np

def release_particles(grid_name, domain):
    """Function to create the lats and lons for the release at a given resolution within a specified domain

    Parameters
    ----------
    grid_name : string
        string to use for e.g., 1-64grid
    domain : list or array
        spatial domain of particle release e.g. domain = [360.-12, 360.-8, 32., 36.] #lomin, lomax, lamin, lamax

    Returns
    -------
    lons, lats
        arrays of longitude and latitude for release

    Raises
    ------
    ValueError
        Value error is raised if the correct configuration of grid resolution is not provided.
    """
    ####################
    # Defining grid of starting particles:
    if grid_name == "1-8grid":
        step = .125  # degrees
    elif grid_name == "1-64grid":
        step = 0.015625  # 1./64degrees
    else:
        raise ValueError("check the value of grid_name")

    lons, lats = np.meshgrid(np.arange(
        domain[0], domain[1]+step, step), np.arange(domain[2], domain[3]+step, step))
    ####################
    return lons, lats


def parcels_simulation(datetime_in, lons, lats, simu_length, filename, outname):
    """
    datetime_in: e.g. datetime(2019, 10, 1, 0, 0)
    simu_length: in days e.g. 15.
    filename: e.g. '../validation/' + 'datos_Laura.nc'
    outname: e.g. '../examples/' + "Particle_AZO_fFTLE_" + grid_name + "_" + str(nmonth).zfill(2) + str(start_day).zfill(2) + "_" + str(simu_length)[0:2] + "d"
    """
    ####################
    # Parcels simulation

    variables = {'U': 'ugos', 'V': 'vgos'}

    filenames = {'U': filename, 'V': filename}

    dimensions = {'U': {'lat': 'latitude', 'lon': 'longitude', 'time': 'time'},
                  'V': {'lat': 'latitude', 'lon': 'longitude', 'time': 'time'}}

    fieldset = FieldSet.from_netcdf(filenames, variables, dimensions)

    pset = ParticleSet(fieldset=fieldset, pclass=JITParticle,
                       lon=lons, lat=lats, time=datetime_in)  # 30))

    output_file = pset.ParticleFile(name=outname, outputdt=timedelta(hours=6))

    # minutes=6*60
    pset.execute(AdvectionRK4, runtime=timedelta(days=simu_length), dt=timedelta(hours=6),
                 output_file=output_file)  # recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle},

    ####################
