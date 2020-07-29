from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


import rhinoscriptsyntax as rs
from System import Array
import Pachyderm_Acoustic.Utilities.RC_PachTools as pt

from compas.utilities import geometric_key

def make_mic_map(mics):
    m = {geometric_key(mic): {'index':i, 'xyz': mic} for i, mic in enumerate(mics)}
    return m


def pach_assign_material(guid, abs, sct, trn):
    abs = Array[int](abs)
    sct = Array[int](sct)
    trn = Array[int](trn)
    pt.Material_SetByObject(guid, abs, sct, trn)

def assign_materials_by_layer(lay_dict):
    for lay in lay_dict:
        srfs = rs.ObjectsByLayer(lay)
        abs = lay_dict[lay]['abs']
        sct = lay_dict[lay]['sct']
        trn = lay_dict[lay]['trn']
        for srf in srfs:
            pach_assign_material(srf, abs, sct, trn)