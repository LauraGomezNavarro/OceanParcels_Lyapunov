# Validation


## Objective: validate and compare the python FTLE function with a FTLE fortran code and FSLE matlab code.

## Sample data : 
Geostrophic currents downloaded from CMEMS.  They are a L4 level processing product. Data is available from 1993 to 2020.
Source link : https://resources.marine.copernicus.eu/?option=com_csw&view=details&product_id=SEALEVEL_GLO_PHY_L4_REP_OBSERVATIONS_008_047 

* Sample dataset: 
  * filename : datos_Laura.nc
  * temporal coverage : October - December 2019
  * spatial coverage : lomin=-35; lomax=-18; lamin=30; lamax=40
  * Date of FTLEs and FSLEs calculation: 01/11/2019. 
  * Calculation parameters:
    * d0 = (spatial separation)
    * dt = (timestep)
    * T  =  (time period)
