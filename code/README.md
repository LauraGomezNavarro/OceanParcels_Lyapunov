# Python FTLE code

## Theory

FTLE = $\frac{ln(r)}{T}$ <br>

; r = $\frac{\Delta f}{\Delta i}$ <br> 
; T = time passed

## Algorithm implementation

### Parcels simulation

Let's say you want to calculate the FTLE field for the 1st of June with a particle advection time of 15 days.  You will first need to run your OceanParcels simulations for :

* **Forward in time FTLE (repelling) :** You release particle on a regular grid (the grid spacing will be your {\Delta i}$ in the equation above), and you advect them using your velocity fields (e.g. ocean model outputs).  You run this simulation from the 1st of June to the 15th of June.  The calculated FTLE values are then plotted on the initial regular grid positions, and represent the forward FTLE on the 1st of June.

* **Backward in time FTLE (attracting) :** You release particle on a regular grid (the grid spacing will be your {\Delta i}$ in the equation above), and you advect them using your velocity fields (e.g. ocean model outputs).  This time, as it is backward in time, you will use your velocity values x -1 (going in the opposite direction). You run this simulation from the 1st of June to the 15th of May. The calculated FTLE values are then plotted on the initial regular grid positions, and represent the backward FTLE on the 1st of June.

### FTLE calculation from OceanParcels outputs



## Validation

## Example
