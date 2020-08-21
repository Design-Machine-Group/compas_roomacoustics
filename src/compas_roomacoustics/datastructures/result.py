from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


TPL = """
################################################################################
compas_roomacoustics Result
################################################################################

Reciever
---------
{0}

Type
----
{1}

EDT
---
{2}

T30
---
{3}

STI
---
{4}

"""


class Result(object):

    def __init__(self, receiver, name='RoomResult', type=None):

        self.receiver   = receiver
        self.etc        = None
        self.t30        = None
        self.edt        = None
        self.sch_int    = None
        self.sti        = None
        self.type       = type

    def __str__(self):
        return TPL.format(self.receiver, self.type, self.edt, self.t30, self.sti)


if __name__ == '__main__':
    pass
