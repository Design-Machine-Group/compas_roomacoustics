from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas_roomacoustics.room import Room
try:
    import rhinoscriptsyntax as rs
except:
    pass


def room_from_rhino(frequencies, srf_layers, srf_mat, src_layer, mic_layer):

    recs = [rs.PointCoordinates(pt) for pt in rs.ObjectsByLayer(src_layer)]
    
    srfs = rs.ObjectsByLayer('reflectors')
    
    srf_ = rs.ObjectsByLayer('back_srf')

    room = Room()
    room.add_frequencies(frequencies)


    room.add_fib_source([40, 20, 2], power=.1)

    room.add_spherical_recs(recs, radius=.3)

    absorption= {fk: .2 for fk in room.freq.values()}
    room.add_material('mat1', absorption)
    room.add_room_surfaces(srfs, 'mat1', True)

    absorption = {fk: .7 for fk in room.freq.values()}
    room.add_material('mat2', absorption)
    room.add_room_surfaces(srf_, 'mat2', True)

    return room

if __name__ == '__main__':
    for i in range(50): print('')
    rs.CurrentLayer('Default')
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))
    frequencies = range(100, 150, 3)

    srf_layers = ['walls', 'floor', 'ceiling']

    abs= {fk: .2 for fk in room.freq.values()}
    walls = {}
    floor = {}
    ceiling = {}
    srf_mat = [walls, floor, ceiling]
    src_layer = 'src'
    mic_layer = 'mics'
    room_from_rhino(frequencies, srf_layers, srf_mat, src_layer, mic_layer)
