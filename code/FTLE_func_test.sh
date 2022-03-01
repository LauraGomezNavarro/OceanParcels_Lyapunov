#/bin/sh

# SGE: the job name
#$ -N Azores_eNATL60_FTLE_MONTH_wtides_0601
#
# The requested run-time, expressed as (xxxx sec or hh:mm:ss)
#$ -l h_rt=02:00:00
#
# SGE: your Email here, for job notification
#$ -M l.gomeznavarro@uu.nl
#
# SGE: when do you want to be notified (b : begin, e : end, s : error)?
#$ -m es
#
# SGE: output in the current working dir
#$ -cwd    
#

cd /nethome/gomez023/parcels_Azores/FTLE/
python3 -c 'from FTLE_func_test import *; FTLE(filename='/data/oceanparcels/output_data/data_LauraGN/outputs_parcels/wtides/monthly/' + 'Particle_AZO_grid100000p_wtides_0601_hourly_MONTH.nc', Td=30., step=0.04, domain=[-35, -18, 30, 40], savename='FTLE_wtides_0601.npz')'
