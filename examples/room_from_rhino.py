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

abs_wall= {62: .5, 125:.5, 250:.5, 500:.5, 1000:.5, 2000:.5, 4000:.5, 8000:.5}
mwalls = {'abs': abs_wall, 'sct': sct, 'trn': trn}

abs_floor= {62: .5, 125:.5, 250:.5, 500:.5, 1000:.5, 2000:.5, 4000:.5, 8000:.5}
mfloor = {'abs': abs_floor, 'sct': sct, 'trn': trn}

abs_cei= {62: .5, 125:.5, 250:.5, 500:.5, 1000:.5, 2000:.5, 4000:.5, 8000:.5}
mceiling = {'abs': abs_cei, 'sct': sct, 'trn': trn}

abs_box= {62: .5, 125:.5, 250:.5, 500:.5, 1000:.5, 2000:.5, 4000:.5, 8000:.5}
mbox = {'abs': abs_box, 'sct': sct, 'trn': trn}

abs_glass= {62: .5, 125:.5, 250:.5, 500:.5, 1000:.5, 2000:.5, 4000:.5, 8000:.5}
mglass = {'abs': abs_glass, 'sct': sct, 'trn': trn}

walls = {'layer': 'walls', 'material': mwalls, 'is_boundary': True}
floor = {'layer': 'floor', 'material': mfloor, 'is_boundary': True}
ceiling = {'layer': 'ceiling', 'material': mceiling, 'is_boundary': True}
glass = {'layer': 'glass', 'material': mglass, 'is_boundary': True}
box = {'layer': 'box', 'material': mbox, 'is_boundary': False}

srfs_dict = {'walls': walls,
             'floor': floor, 
             'ceiling': ceiling,
             'box': box,
             'glass':glass}

src_layer = 'src'
src_power = .1
mic_layer = 'mics'
room = room_from_rhino(frequencies, srfs_dict, src_layer, src_power,  mic_layer)
room.to_json(filepath)
print(room)