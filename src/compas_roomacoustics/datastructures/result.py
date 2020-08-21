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

    def __init__(self, receiver, name='RoomResult', type=None):

        self.receiver   = receiver
        self.name       = name
        self.type       = type
        self.etc        = []
        self.t30        = []
        self.edt        = []
        self.sch_int    = []
        self.sti        = []


    def __str__(self):
        return TPL.format(self.receiver, self.type, self.edt, self.t30, self.sti)


    @property
    def data(self):
        """dict : A data dict representing the result for serialisation.
        """
        data = {'name'          : self.name,
                'receiver'      : self.receiver,
                'type'          : self.type,
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

    # @data.setter
    # def data(self, data):
    #     self.name           = data.get('name') or {}
    #     self.scattering     = data.get('scattering') or {}
    #     self.transparency   = data.get('transparency') or {}

    #     absorption  = data.get('absorption') or {}
    #     self.absorption = {}
    #     for akey in absorption:
    #         self.absorption[literal_eval(akey)] = absorption[akey]

    #     scattering  = data.get('scattering') or {}
    #     self.scattering = {}
    #     for akey in scattering:
    #         self.scattering[literal_eval(akey)] = scattering[akey]

    #     transparency  = data.get('transparency') or {}
    #     self.transparency = {}
    #     for akey in transparency:
    #         self.transparency[literal_eval(akey)] = transparency[akey]

    # @classmethod
    # def from_data(cls, data):
    #     """Construct a material from structured data.

    #     Parameters
    #     ----------
    #     data : dict
    #         The data dictionary.

    #     Returns
    #     -------
    #     object
    #         An object of the type of ``cls``.

    #     Note
    #     ----
    #     This constructor method is meant to be used in conjuction with the
    #     corresponding *to_data* method.
    #     """
    #     name = data['name']
    #     scatteting = data['scatteting']
    #     transparency = data['transparency']
    #     absorption = data['absorption']
    #     material = cls(name, absorption, scatteting, transparency)
    #     return material

if __name__ == '__main__':
    pass
