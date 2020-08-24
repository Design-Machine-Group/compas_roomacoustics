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

abs_wall= {62: .17, 125:.15, 250:.1, 500:.06, 1000:.04, 2000:.04, 4000:.05, 8000:.06}
mwalls = {'abs': abs_wall, 'sct': sct, 'trn': trn}

abs_floor= {62: .03, 125:.04, 250:.04, 500:.07, 1000:.06, 2000:.06, 4000:.07, 8000:.07}
mfloor = {'abs': abs_floor, 'sct': sct, 'trn': trn}

abs_cei= {62: .01, 125:.01, 250:.01, 500:.02, 1000:.02, 2000:.02, 4000:.05, 8000:.04}
mceiling = {'abs': abs_cei, 'sct': sct, 'trn': trn}

abs_box= {62: .35, 125:.73, 250:.83, 500:.93, 1000:.94, 2000:.35, 4000:.3, 8000:.1}
mbox = {'abs': abs_box, 'sct': sct, 'trn': trn}

abs_glass= {62: .22, 125:.18, 250:.06, 500:.04, 1000:.03, 2000:.02, 4000:.02, 8000:.02}
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