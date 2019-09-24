"""
********************************************************************************
compas_roomacoustics
********************************************************************************

.. currentmodule:: compas_roomacoustics


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
import sys


__author__ = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__ = 'Tomas Mendez Echenagucia - University of Washington'
__license__ = 'MIT License'
__email__ = 'tmendeze@uw.edu'
__version__ = '0.1.0'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))


__all__ = ['HOME', 'DATA', 'DOCS', 'TEMP']
