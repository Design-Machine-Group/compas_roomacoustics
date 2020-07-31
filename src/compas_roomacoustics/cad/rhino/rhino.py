from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

for i in range(50): print()

from compas_roomacoustics.datastructures import Room

try:
    import rhinoscriptsyntax as rs
except:
    pass


def room_from_rhino(frequencies, srf_dict, src_layer, src_power, mic_layer):
    
    room = Room()
    room.add_frequencies(frequencies)

    # add mics -------------------------------------------------------------
    mics = [list(rs.PointCoordinates(pt)) for pt in rs.ObjectsByLayer(mic_layer)]
    room.add_spherical_recs(mics, radius=.3)

    # add source -----------------------------------------------------------
    sxyz = list(rs.PointCoordinates(rs.ObjectsByLayer(src_layer)[0]))
    room.add_fib_source(sxyz, power=src_power)

    # add surfaces ---------------------------------------------------------

    for key in srf_dict:
        layer = srf_dict[key]['layer']
        mat = srf_dict[key]['material']
        is_boundary = srf_dict[key]['is_boundary']
        guids = rs.ObjectsByLayer(layer)
        srf_pts = []
        for guid in guids:
            pts = [[pt.X, pt.Y, pt.Z] for pt in rs.SurfacePoints(guid)]
            pts = [pts[0], pts[1], pts[3], pts[2]]
            srf_pts.append(pts)
        room.add_material(layer, mat['abs'], mat['sct'], mat['trn'])
        room.add_room_surfaces(srf_pts, layer, is_boundary)

    return room

if __name__ == '__main__':

    import os

    path = 'c:\\users\\tmendeze\\documents\\uw_code\\compas_roomacoustics\\temp'
    filename = 'simple_box.json'
    filepath = os.path.join(path, filename)


    frequencies = [62, 125, 250, 500, 1000, 2000, 4000, 8000]

    srf_layers = ['walls', 'floor', 'ceiling']

    sct = {fk: .2 for fk in frequencies}
    trn = {fk: .0 for fk in frequencies}

    abs_wall= {fk: .05 for fk in frequencies}
    mwalls = {'abs': abs_wall, 'sct': sct, 'trn': trn}

    abs_floor= {fk: .3 for fk in frequencies}
    mfloor = {'abs': abs_floor, 'sct': sct, 'trn': trn}

    abs_cei= {fk: .5 for fk in frequencies}
    mceiling = {'abs': abs_cei, 'sct': sct, 'trn': trn}

    walls = {'layer': 'walls', 'material': mwalls, 'is_boundary': True}
    floor = {'layer': 'floor', 'material': mfloor, 'is_boundary': True}
    ceiling = {'layer': 'ceiling', 'material': mceiling, 'is_boundary': True}
    srfs_dict = {'walls': walls, 'floor': floor, 'ceiling': ceiling}

    src_layer = 'src'
    src_power = .1
    mic_layer = 'mics'
    room = room_from_rhino(frequencies, srfs_dict, src_layer, src_power,  mic_layer)
    room.to_json(filepath)
    print(room)