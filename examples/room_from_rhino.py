from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import os

from compas_roomacoustics.cad.rhino import room_from_rhino

path = 'c:\\users\\tmendeze\\documents\\uw_code\\compas_roomacoustics\\data'
filename = 'simple_box_allrecs.json'
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