# Imports
import meep as mp 
import numpy as np
import matplotlib.pyplot as plt 
import os
from pathlib import Path
from gplugins.gmeep.get_meep_geometry import get_meep_geometry_from_component
from gdsfactory.read import import_gds
import gdsfactory as gf
import pathlib
mp.verbosity(3)

res = 20 # the resolution of the simulation in pixels/um
sim_is_3D = False # Turn this to false for a 2D simulation

pwd = pathlib.Path(__file__).parent.resolve()
gds_file = pwd.parent / "files/mmi2x2.gds" # The name of our gds file

# The Parameters for the frequencies we'll be using
lcen = 1.55 # Center wavelength
fcen = 1 / lcen # Center frequency
df = 0.05*fcen # Frequency Diameter

# The thickness of each material in our simulation (only used in 3D simulations)
t_oxide = 1.0
t_Si = 0.22
t_air = 0.78

dpml = 1 # Diameter of perfectly matched layers
cell_thickness = dpml + t_oxide + t_Si + t_air + dpml # Cell thickness

# Materials used in the simulation
Si = mp.Medium(index=3.45)
SiO2 = mp.Medium(index=1.444)

# Sets the min and max values for the cell and the silicon. Our simulation will be centered at y=0
cell_zmax = 0.5*cell_thickness if sim_is_3D else 0
cell_zmin = -0.5 * cell_thickness if sim_is_3D else 0

# Create a 2D array to hold the S-Parameters for the device
n_ports = 4 # The number of ports, also the size of our array
s_params = np.zeros((n_ports, n_ports))

mode_parity = mp.NO_PARITY if sim_is_3D else mp.EVEN_Y + mp.ODD_Z

from gdsfactory.technology import LayerLevel, LayerStack
layers = dict(core=LayerLevel(
            layer=(1,0),
            thickness=t_Si,
            zmin=-t_Si/2,
            material="si",
            mesh_order=2,
            sidewall_angle=0,
            width_to_z=0.5,
            orientation="100",)
              )
layer_stack = LayerStack(layers=layers)

mmi_comp = import_gds(gds_file)
geometry = get_meep_geometry_from_component(mmi_comp, is_3d=sim_is_3D, wavelength=lcen, layer_stack=layer_stack)
# Use this to modify the material of the loaded geometry if needed.
# geometry = [mp.Prism(geom.vertices, geom.height, geom.axis, geom.center, material=mp.Medium(index=3.45)) for geom in geometry]

# ###################################################
# Now we actually import the geometry
cell_x = 32
cell_y = 6
cell_z = 3

port_xsize = 0
port_ysize = 1
port_zsize = 0.5

port_xdisp = 13
port_ydisp = (0.75+0.5)/2

port_size = mp.Vector3(port_xsize, port_ysize, port_zsize) if sim_is_3D else mp.Vector3(port_xsize, port_ysize, 0)
cell = mp.Vector3(cell_x, cell_y, cell_z) if sim_is_3D else mp.Vector3(cell_x, cell_y, 0)

port1 = mp.Volume(center=mp.Vector3(-port_xdisp,-port_ydisp,0), size=port_size)
port2 = mp.Volume(center=mp.Vector3(-port_xdisp,port_ydisp,0), size=port_size)
port3 = mp.Volume(center=mp.Vector3(port_xdisp,port_ydisp,0), size=port_size)
port4 = mp.Volume(center=mp.Vector3(port_xdisp,-port_ydisp,0), size=port_size)
source1 = mp.Volume(center=port1.center-mp.Vector3(x=0.5),size=port_size)
source2 = mp.Volume(center=port4.center+mp.Vector3(x=0.5), size=port_size)

subtraction_geom = [mp.Block(size=mp.Vector3(mp.inf, 0.5, t_Si), material=Si)]
subtraction_cell = mp.Vector3(5, 4, cell_z if sim_is_3D else 0)
subtraction_sources = [
    mp.EigenModeSource(
            src = mp.GaussianSource(fcen, fwidth=df),
            volume=mp.Volume(center=mp.Vector3(-0.5,0,0), size=port_size),
            eig_band=1,
            eig_parity = mode_parity,
            eig_match_freq = True,
    )
]

subtraction_sim = mp.Simulation(
    resolution=res,
    cell_size=subtraction_cell,
    boundary_layers=[mp.PML(dpml)],
    sources=subtraction_sources,
    geometry=subtraction_geom,
    default_material=SiO2
)

subtraction_monitor_region = mp.FluxRegion(center=mp.Vector3(0), size=port_size)
subtraction_monitor = subtraction_sim.add_flux(fcen, 0, 1, subtraction_monitor_region)

plot_plane = mp.Volume(center=mp.Vector3(z=0), size=mp.Vector3(cell.x, cell.y, 0))
subtraction_sim.plot2D(output_plane=plot_plane if sim_is_3D else None)
subtraction_sim.run(until_after_sources=mp.stop_when_dft_decayed)

subtraction_data = subtraction_sim.get_flux_data(subtraction_monitor)
norm_mode_coeff = subtraction_sim.get_eigenmode_coefficients(subtraction_monitor, [1], mode_parity).alpha[0,0,0]

# Set up the first source for the simulation. I'll start with port1 (the lower left)
sources = [
    mp.EigenModeSource(
            src = mp.GaussianSource(fcen, fwidth=df),
            volume=source1,
            eig_band=1,
            eig_parity = mode_parity,
            eig_match_freq = True,
    )
]

# Create Simulation
sim = mp.Simulation(
    resolution=res, # The resolution, defined further up
    cell_size=cell, # The cell size, taken from the gds
    boundary_layers=[mp.PML(dpml)], # the perfectly matched layers, with a diameter as defined above
    sources = sources, # The source(s) we just defined
    geometry = geometry, # The geometry, from above
    default_material=SiO2
)

# Adds mode monitors at each of the ports to track the energy that goes in or out

mode_monitor_1 = sim.add_mode_monitor(fcen, 0, 1, mp.ModeRegion(volume=port1))
mode_monitor_2 = sim.add_mode_monitor(fcen, 0, 1, mp.ModeRegion(volume=port2))
mode_monitor_3 = sim.add_mode_monitor(fcen, 0, 1, mp.ModeRegion(volume=port3))
mode_monitor_4 = sim.add_mode_monitor(fcen, 0, 1, mp.ModeRegion(volume=port4))

sim.load_minus_flux_data(mode_monitor_1, subtraction_data)

# Plot the simulation
plot_plane = mp.Volume(center=mp.Vector3(z=0), size=mp.Vector3(cell.x, cell.y, 0))
# sim.plot2D(output_plane=plot_plane if sim_is_3D else None) # No parameters are needed for a 2D simulation. 

