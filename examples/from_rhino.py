import os
import sys
import time

sys.path.append('/src')

import rhinoscriptsyntax as rs

import compas_roomacoustics
from compas_roomacoustics.room import Room
from compas_roomacoustics.raytracer import shoot_rays
from compas_roomacoustics.ray_analysis import make_histogram
from compas_roomacoustics.ray_analysis import spl_from_intensity
from compas_roomacoustics.material import Material

from compas_roomacoustics import plot_results as plot
reload(plot)
from compas_roomacoustics.plot_results import visualize_rays
from compas_roomacoustics.plot_results import plot_spl

from compas_roomacoustics import ray_analysis
reload(ray_analysis)
from compas_roomacoustics.ray_analysis import make_histogram


for i in range(50): print('')
rs.CurrentLayer('Default')
rs.DeleteObjects(rs.ObjectsByLayer('Default'))

tic = time.time()

pts = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer('receivers')]
srfs = rs.ObjectsByLayer('reflectors')
srf_ = rs.ObjectsByLayer('back_srf')

r = Room()
r.num_rays = 10000
r.add_frequencies(range(100,102))
srcpt = list(rs.PointCoordinates(rs.ObjectsByLayer('source')[0]))
r.add_fib_source(srcpt, power=.1)

r.add_spherical_recs(pts, radius=.3)

absorption= {fk: .2 for fk in r.freq.values()}
r.add_material('mat1', absorption)
r.add_room_surfaces(srfs, 'mat1', True)

absorption = {fk: .7 for fk in r.freq.values()}
r.add_material('mat2', absorption)
r.add_room_surfaces(srf_, 'mat2', True)

shoot_rays(r)
# visualize_rays(r, keys= None, ref_order=None, layer='Default', dot=None)

histo, intsty = make_histogram(r)
spl = spl_from_intensity(intsty)

toc = time.time()

plot_spl(r, spl, 100)
print(toc - tic)
