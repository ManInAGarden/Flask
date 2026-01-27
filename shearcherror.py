import os.path
from pathlib import Path

from build123d import *
from ocp_vscode import *

from bd_warehouse.thread import PlasticBottleThread

# ASTM D2911
thread_size = "M13SP415"
outer_wall  = 1 * MM

# ======================================================================
# Create the external threads (threaded bar)
# ======================================================================

external_threads = PlasticBottleThread(thread_size, external=True)

neck_radius = external_threads.root_radius

external_cylinder = Circle(neck_radius + 0.001 * MM)
external_cylinder = extrude(external_cylinder, external_threads.height + 10)

male_thread = external_cylinder + external_threads

# ======================================================================
# Create the internal threads (cap, threads on the inside)
# ======================================================================

internal_threads = PlasticBottleThread(thread_size, external=False)

neck_radius = internal_threads.root_radius

tube  = Circle(neck_radius + outer_wall)
tube -= Circle(neck_radius - .001 * MM)
cap   = extrude(tube, amount=internal_threads.height + 10)
cap  += internal_threads

# ======================================================================
# Show results
# ======================================================================

show(cap, Pos(0, 0, -10) * male_thread)
show_all()