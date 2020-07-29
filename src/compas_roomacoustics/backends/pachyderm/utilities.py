from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


import json

def etcs_to_json(filepath, etcs):
    for mic in etcs:
        for oct in etcs[mic]:
            etcs[mic][oct] = list(etcs[mic][oct])

    with open(filepath, 'w+') as fp:
        json.dump(etcs, fp)