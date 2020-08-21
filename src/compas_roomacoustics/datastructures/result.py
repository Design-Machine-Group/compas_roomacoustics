from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ast import literal_eval

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

    def __init__(self, receiver, name='RoomResult', restype='GeneralResult'):

        self.receiver   = receiver
        self.name       = name
        self.restype    = restype
        self.etc        = []
        self.t30        = []
        self.edt        = []
        self.sch_int    = []
        self.sti        = []


    def __str__(self):
        return TPL.format(self.receiver, self.restype, self.edt, self.t30, self.sti)


    @property
    def data(self):
        """dict : A data dict representing the result for serialisation.
        """
        data = {'name'          : self.name,
                'receiver'      : self.receiver,
                'restype'       : self.restype,
                'etc'           : {},
                't30'           : {},
                'edt'           : {},
                'sch_int'       : {},
                'sti'           : self.sti,
                }

        for key in self.etc:
            data['etc'][literal_eval(str(key))] = self.etc[key]

        for key in self.t30:
            data['t30'][literal_eval(str(key))] = self.t30[key]

        for key in self.edt:
            data['edt'][literal_eval(str(key))] = self.edt[key]

        for key in self.sch_int:
            data['sch_int'][literal_eval(str(key))] = self.sch_int[key]

        return data

    @data.setter
    def data(self, data):
        self.name           = data.get('name') or {}
        self.receiver       = data.get('receiver') or {}
        self.restype        = data.get('restype') or {}
        self.sti            = data.get('sti') or {}

        etc  = data.get('etc') or {}
        self.etc = {}
        for key in etc:
            self.etc[literal_eval(key)] = etc[key]

        t30  = data.get('t30') or {}
        self.t30 = {}
        for key in t30:
            self.t30[literal_eval(key)] = t30[key]

        edt  = data.get('edt') or {}
        self.edt = {}
        for key in edt:
            self.edt[literal_eval(key)] = edt[key]

        sch_int  = data.get('sch_int') or {}
        self.sch_int = {}
        for key in sch_int:
            self.sch_int[literal_eval(key)] = sch_int[key]


    @classmethod
    def from_data(cls, data):
        """Construct a result from structured data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.
        """
        name = data['name']
        receiver = data['receiver']
        restype = data['restype']

        result = cls(receiver, name, restype=restype)
        result.data = data
        return result

if __name__ == '__main__':
    pass
